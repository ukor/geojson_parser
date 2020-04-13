from elasticsearch import Elasticsearch
from geo_parser.parse_admin_area import AdminArea
from geo_parser.parse_district_geojson import District
from geo_parser.parse_area_geojson import Area
from geo_parser.es_config import ConfigElasticSearch


if __name__ == "__main__":
    # initiate elastic search
    es = Elasticsearch()
    _index = "homeknock_places"
    _index_settings = ConfigElasticSearch().settings()
    _delete_index = es.indices.delete(index=_index, ignore=[400])
    print("******************************************************")
    print(_delete_index, "delete index")
    print("******************************************************")
    _create_index = es.indices.create(body=_index_settings, index=_index, ignore=[400])
    print("=====================================================================")
    print(_create_index, _index_settings)
    print("=====================================================================")
    
    area = Area("./postcode-boundaries.json").parse()
    print("Done with area =>", area)
    district = District("./postcode_districts.json").parse()
    print("Done with district =>", district)
    # admin = AdminArea("./uk/").parse()
    area = 124
    admin = 0

    print(f"Postcode Area = {area}")
    print(f"District = {district}")
    print(f"Adminstrative Area = {admin}")
    print(f"Created {area + district + admin} files.")

    #  Refresh the index
    _ref = es.indices.refresh(index=_index)
    print(_ref, "refresh")

