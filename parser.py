from pathlib import Path
from os.path import join
from elasticsearch import Elasticsearch
from geojson_parse.parse_admin_area import AdminArea
from geojson_parse.parse_district_geojson import District
from geojson_parse.parse_area_geojson import Area
from geojson_parse.es import es_client


if __name__ == "__main__":

    home_dir = str(Path.home())
    print(home_dir)
    _es_client = Elasticsearch()
    es = es_client(es_instance=_es_client)
    # es.delete_index()
    es.create_index()

    area = Area(es_client, source_path, dest_path "./postcode-boundaries.json").parse()
    # print("Done with area =>", area)
    # district = District("./postcode_districts.json").parse()
    # print("Done with district =>", district)
    # admin = AdminArea( es_client = _es_client , source_dir_path, dest_dir_path "./uk/").parse()
    # area = 124
    # admin = 0

    # print(f"Postcode Area = {area}")
    # print(f"District = {district}")
    # print(f"Adminstrative Area = {admin}")
    # print(f"Created {area + district + admin} files.")

    #  Refresh the index


