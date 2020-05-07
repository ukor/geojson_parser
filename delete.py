import time

from es.es import es_client
from es.es_config import ConfigElasticSearch
from es_instance import es_instance

scopes = ["place", "admin", "london_borough", "area", "postcode_area", "ward", "parish"]

for scope in scopes:
    es_client.delete_by_query(scope)
    time.sleep(1.30)
