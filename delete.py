import time

from es.es import es_client
from es.es_config import ConfigElasticSearch
from es_instance import es_instance

# scopes = ["place", "admin", "london_borough", "area", "postcode_area", "ward", "parish"]
scopes = ["postcode_area"]

for scope in scopes:
    _es_instance = es_instance()

    _es_client = es_client(es_instance=_es_instance, es_index="hk_places")

    _es_client.delete_by_query(scope)
    time.sleep(1.30)
