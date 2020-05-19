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

from config.config import POLYGON_DESTINATION

from es.es import es_client
from es.es_config import ConfigElasticSearch
from es_instance import es_instance

from helpers import removePuntautions, hashFileName
class London:
    def __init__(self, *, src_path: str, dest_path: str, es_instance):
        home_dir = str(Path.home())
        self.src_path = src_path
        self.es = es_instance
        self.dest_path = f"{home_dir}/polygons" if dest_path in [None, False, ""] else dest_path
        self.write_count = 0
        self.scope = "place"


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
            _scope = self.scope
            for feature in features:
                # write to a new file using place id as file name
                if _props["name"].lower() != "london":
                    _props = feature["properties"]
                    _id = hashFileName(removePuntautions(_props["name"]).lower().replace(" ", "_"))
                    file_name = f'{_scope}_{_id}'
                    _geo_json = {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type": "Feature",
                                "properties": {
                                    "name": _props["name"],
                                    "gss_code": "",
                                    "district_code": "",
                                    "district_name": "",
                                },
                                "geometry": feature["geometry"]
                            }
                        ],
                    }

                    # Index to database
                    print(f"Indexing {_props['name']} with id {file_name}")
                    es_client = self.es
                    es_client.add_doc(
                        id=_id,
                        name=_props["name"],
                        official_name=f'{_props["name"].title()}, UK',
                        area="Greater London",
                        polygon_file_name=file_name,
                        scope=_scope)

                    self._write_file(file_name=file_name, geojson=_geo_json)
                    print(
                        f"Start writing geoJSON from {Path(self.src_path).name} to {file_name}.json")
                    time.sleep(0.25)


    def _write_file(self, *,file_name, geojson):
        """_write_file - Write polygons into file"""
        _file_path = join(self.dest_path, file_name) + ".json"
        # write into file as json
        with open(_file_path, "w") as json_file:
            json.dump(geojson, json_file, use_decimal=True, indent=2,
                    separators=(",", ":"), encoding="utf-8")

        self.write_count += 1


if __name__ == "__main__":
    _es_instance = es_instance()

    _es_client = es_client(es_instance=_es_instance, es_index="places")
    # do not uncomment, - it will delete the entire database...
    # ...action can't be undone, it is here for clean up purpose only
    _es_client.delete_index()
    _es_client.create_index()
    _src = f"./raw/london.json"
    london = London(src_path=_src, dest_path=POLYGON_DESTINATION, es_instance=_es_client)
    area_count = london.parse()
    print(f"Created and Indexed {area_count} areas")
    _es_client.refresh_index()
