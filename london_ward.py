"""
    Extract London Wards boundary from geoJSON (JSON) file
    index them in elastic search
    author: j.ukor
    organization: Home knock
"""
from pathlib import Path
from os.path import join
import time

import certifi
from elasticsearch import Elasticsearch, RequestsHttpConnection
import simplejson as json
import ijson
from requests_aws4auth import AWS4Auth
from shapely.geometry.polygon import Polygon

from config.config import POLYGON_DESTINATION

from es.es import es_client
from es.es_config import ConfigElasticSearch
from es_instance import es_instance

from helpers import removePuntautions, hashFileName, getPoints

from great_london_poly import poly

class Wards:
    def __init__(self, *, src_path: str, dest_path: str, es_instance):
        home_dir = str(Path.home())
        self.src_path = src_path
        self.es = es_instance
        self.dest_path = f"{home_dir}/polygons" if dest_path in [None, False, ""] else dest_path
        self.write_count = 0


    def parse(self):
        # check and create directory
        self._set_path()
        # read files from source and write to a destination dir
        self._read_file()
        return self.write_count


    def _set_path(self):
        """_set_path
            Checks and create path if it does not exist
        """

        if Path(f"{self.src_path}").exists() is not True:
            raise FileNotFoundError(f"Source file {self.src_path} not found.")

        if Path(self.dest_path).exists() is not True:
            # create the directory
            Path(self.dest_path).mkdir(parents=True, exist_ok=True)


    def _read_file(self):
        """_read_file - Read files from source path """

        with open(self.src_path, "rb") as _file:
            obj = ijson.items(_file, "features.item")
            features = (o for o in obj if o["type"] == "Feature")
            _scope = "place"
            _poly = Polygon(poly)
            for feature in features:
                _point = getPoints(feature.get("geometry", {}))
                # restricts polygons to only plcaes in Greater London
                if _poly.contains(_point) or _poly.touches(_point):
                    # write to a new file using place id as file name
                    _props = feature["properties"]
                    _id = hashFileName(removePuntautions(_props["NAME"]).lower().replace(" ", "_"))
                    file_name = f'{_scope}_{_id}'
                    _geo_json = {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type":"Feature",
                                "properties": {
                                    "name": _props["NAME"].title(),
                                    "gss_code": _props["GSS_CODE"],
                                    "district_code": _props["LAGSSCODE"],
                                    "district_name": _props["DISTRICT"],
                                },
                                "geometry": feature["geometry"]
                            }
                        ],
                    }

                    # Index to database
                    print(f"Indexing {_props['NAME']} with id {_props['GSS_CODE']}")
                    es_client = self.es
                    es_client.add_doc(
                        id=_id,
                        name=_props["NAME"],
                        official_name= f'{_props["NAME"].title()}, London, UK',
                        # district= f'{_props["DISTRICT"]}, London',
                        area= "London", # base on feedback - _props["DISTRICT"] =
                        polygon_file_name=file_name,
                        scope=_scope)

                    self._write_file(file_name=file_name, geojson=_geo_json)
                    print(
                        f"Start writing geoJSON from {Path(self.src_path).name} to {file_name}.json")
                    time.sleep(0.25)


    def _write_file(self, *,file_name, geojson):
        """_write_file - Write wards geojson into file"""
        _file_path = join(self.dest_path, file_name) + ".json"
        # write into file as json
        with open(_file_path, "w") as json_file:
            json.dump(geojson, json_file, use_decimal=True, indent=2,
                    separators=(",", ":"), encoding="utf-8")

        self.write_count += 1


if __name__ == "__main__":
    _es_instance = es_instance()

    _es_client = es_client(es_instance=_es_instance, es_index="places")
    # _es_client.delete_index()
    _es_client.create_index()
    _src = f"./raw/London-wards-2018.zip.geojson"
    ward = Wards(src_path=_src, dest_path=POLYGON_DESTINATION, es_instance=_es_client)
    ward_count = ward.parse()
    print(f"Created and Indexed {ward_count} ward")
    _es_client.refresh_index()
