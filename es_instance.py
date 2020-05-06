from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import certifi

from es.es import es_client
from es.es_config import ConfigElasticSearch

from config.config import (ES_ENDPOINT, ENV, AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY, AWS_REGION, POLYGON_DESTINATION)


def es_instance():
    _es_instance = Elasticsearch(timeout=300)
    if ENV != "dev":
        aws_auth = AWS4Auth(
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY,
            AWS_REGION,
            "es")
        _es_instance = Elasticsearch(
            timeout=300, hosts=ES_ENDPOINT,
            port=443, use_ssl=True,
            http_auth=aws_auth,
            connection_class= RequestsHttpConnection,
            ca_certs=certifi.where())

    return _es_instance
