import time
import simplejson as json
from os import listdir, rename
from os.path import isfile, join
import ijson
from .es import es_client


class AdminArea:

    def __init__(self, es_client, source_path, dest_path):
        self.write_count = 0
        self.es = es_client
        self._dir_path = source_path
        self.destination_dir = dest_path or  "./mapTestBackend/uk_boundaries"

    def parse(self) -> int:
        _dir_path = self._dir_path
        for _file in listdir(_dir_path):
            full_path = join(_dir_path, _file)
            if isfile(full_path):
                new_name = full_path.strip().replace(" ", "_")
                rename(full_path, new_name)
                self._read_file(new_name)

        return self.write_count


    def _read_file(self, file_path):
        with open(file_path, "rb") as _file:
            obj = ijson.items(_file, "features.item")
            features = (o for o in obj if o["type"] == "Feature")
            for feature in features:
                # write to a new file using place id as file name
                _props = feature["properties"]
                file_name = _props["id"]
                del _props["alltags"]

                print("Indexing {_props['name']} with id _props['id'] ")

                es_client(es_instance=self.es).add_doc(
                    id=_props["id"],
                    name=_props["name"],
                    official_name=_props["name"],
                    polygon_file_name=file_name,
                    scope="administrative")

                _geoJson = {
                    "type": "FeatureCollection",
                    "features": [feature]
                }
                self._write_file(file_name, _geoJson)
                print(
                    f"Start writing geoJSON from {file_path} to {file_name}.json")
                time.sleep(0.25)


    def _write_file(self, file_name, obj):
        _f_name = file_name.lower().replace("/", "_").replace(" ", "_")
        _file_path = join(self.destination_dir, _f_name) + ".json"
        # write into file as json
        with open(_file_path, "w") as json_file:
            json.dump(obj, json_file, use_decimal=True, indent=2,
                    separators=(",", ":"), encoding='utf-8')

        self.write_count += 1

