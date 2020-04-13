import time
import simplejson as json
from os import listdir, rename
from os.path import isfile, join
import ijson
import pandas as pd
from pymongo import MongoClient
from elasticsearch import Elasticsearch


class District:

    def __init__(self, file_path):
        # initiate elastic search
        self.es = Elasticsearch()
        self.mongoClient = MongoClient('localhost', 27017)
        self.mDB = self.mongoClient['homeKnock']
        self.collection = self.mDB['postcode_district_town']

        self.write_count = 0
        self._file_path = file_path
        self.destination_dir = "./mapTestBackend/districts"
        self._index = "homeknock_places"

        # old index - todo [@ukor]: delete 
        # self._index = "homeknock_geodata"

    def parse(self) -> int:
        _file_path = self._file_path
        new_name = _file_path.strip().replace(" ", "_")
        self._read_file(new_name)
        return self.write_count

    def csv_to_json(self, filename):
        data = pd.read_csv(filename)
        d = data.to_dict('records')
        return d

    def save_to_mongoDB():
        j = self.csv_to_json("~/Documents/upwork/homeknock/_data/postcode_districts_with_towns.csv")
        self.collection.insert_many(j)


    def _get_district_from_mongodb(self, district):
        collection = self.collection
        towns = collection.find({"Postcode": district})
        ts = []
        for town in towns: 
            ts.append(str(town["Town"]))

        # t = ", ".join(ts)
        # print(f"From mongoDb => {t}")
        return ts

    def _get_district_from_api(self, district):
        pass

    def _read_file(self, file_path):
        with open(file_path, "rb") as _file:
            obj = ijson.items(_file, "features.item")
            features = (o for o in obj if o["type"] == "Feature")
            for feature in features:
                _props = feature['properties']
                # write to a new file
                file_name = _props['name'].lower()
                res = self.es.index(index=self._index, id=file_name, body={
                    "id": _props['name'].lower(),
                    "name": _props["name"],
                    "official_name": _props["name"],
                    "polygon_file_name": file_name,
                    "scope": "postcode_district",
                })
                print(res["result"], _props['name'].lower(), "doc: elastic search")

                # index each district name
                _districts = self._get_district_from_mongodb(_props["name"])
                _props['districts'] = _districts
                for district in _districts:
                    _doc_id = f'{district}_{_props["name"]}'.lower().replace(" ","_")
                    doc = {
                        "id": _doc_id,
                        "name": f'{district} {_props["name"]}',
                        "official_name": f'{district} {_props["name"]}',
                        "polygon_file_name": file_name,
                        "scope": "postcode_district",
                    }
                    res = self.es.index(index=self._index, id=_doc_id, body=doc)
                    print(res["result"], _doc_id, "doc: elastic search")

                _geoJson = {
                    "type": "FeatureCollection",
                    "features": [feature]
                }

                self._write_file(file_name, _geoJson)
                print(
                    f"Wrote geoJSON from {file_path} to {file_name}.json")
                time.sleep(0.5)

    def _write_file(self, file_name, obj):
        _f_name = file_name.lower().replace("/", "_").replace(" ", "_")
        # print(f"Writing geoJSON to => {_f_name}")
        _file_path = join(self.destination_dir, _f_name)+".json"
        with open(_file_path, "w") as json_file:
            json.dump(obj, json_file, use_decimal=True, indent=2,
                    separators=(",", ":"), encoding='utf-8')

        self.write_count += 1


