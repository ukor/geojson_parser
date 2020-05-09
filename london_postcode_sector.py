""" Parse and Index all postcodes (Sectors) in Greater London """
from pathlib import Path
from os.path import join
import time

import certifi
from elasticsearch import Elasticsearch, RequestsHttpConnection
import simplejson as json
import ijson
from requests_aws4auth import AWS4Auth
import kml2geojson
import requests


from config.config import POLYGON_DESTINATION
from es.es import es_client
from es.es_config import ConfigElasticSearch
from es_instance import es_instance

class PostcodeSector:
    def __init__(self, *, src_path: str, dest_path: str, es_instance):
        self.home_dir = str(Path.home())
        self.src_path = src_path
        self.es = es_instance
        self.dest_path = f"{self.home_dir}/polygons" if dest_path in [None, False, ""] else dest_path
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
            _scope = "postcode_sector"
            for feature in features:
                # write to a new file using place id as file name
                _props = feature["properties"]
                place_name = _props["Name"] if _props["Name"].find(", London") < 0 else _props["Name"][:_props["Name"].find(", London")]
                file_name = f'{_scope}_{place_name.lower().replace(" ", "_")}'
                _geo_json = {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type":"Feature",
                            "properties": {
                                "name": place_name,
                            },
                            "geometry": feature["geometry"]
                        }
                    ],
                }

                # Index to database
                print(f"Indexing {_props['Name']} with id {file_name}")
                es_client = self.es
                es_client.add_doc(
                    id=file_name,
                    name=place_name,
                    official_name=place_name,
                    district="London",
                    country="UK",
                    polygon_file_name=file_name,
                    scope=_scope)

                self._write_file(file_name=file_name, geojson=_geo_json)
                print(
                    f"Start writing geoJSON from {Path(self.src_path).name} to {file_name}.json")
                time.sleep(0.25)


    def _write_file(self, *,file_name, geojson):
        """_write_file - Write polygons into file"""
        _f_name = file_name.lower().replace("/", "_").replace(" ", "_")
        _file_path = join(self.dest_path, _f_name) + ".json"
        # write into file as json
        with open(_file_path, "w") as json_file:
            json.dump(geojson, json_file, use_decimal=True, indent=2,
                    separators=(",", ":"), encoding="utf-8")

        self.write_count += 1


if __name__ == "__main__":
    _es_instance = es_instance()

    _es_client = es_client(es_instance=_es_instance, es_index="hk_postcode_sector")
    # _es_client.delete_index()
    _es_client.create_index()
    file_name = "london_postcode_sectors"

    # _kml_src = f"./raw/{file_name}.kml"
    # convert from kml to geoJSON
    # python crashes for large files - ogr2ogr handles the conversion in the terminal
    # kml2geojson.main.convert(_kml_src, "./raw")

    _geojson_src = f"./raw/{file_name}.geojson"

    # Parse and index individual geoJson
    place = PostcodeSector(src_path=_geojson_src, dest_path=POLYGON_DESTINATION, es_instance=_es_client)
    place_count = place.parse()
    print(f"Created and Indexed {place_count} Postcode sector")
    _es_client.refresh_index()
