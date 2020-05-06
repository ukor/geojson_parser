"""
Interface for elastic search
"""

from .es_config import ConfigElasticSearch
# from config.config import ES_INDEX_NAME

class es_client:
    def __init__(self, es_index=None, es_instance):
        self.es = es_instance;
        self._index = "homeknock_places" if es_index in [None, False, "", 0] else es_index


    def delete_index(self):
        es = self.es
        _delete_index = es.indices.delete(index=self._index, ignore=[400])
        print(f"Action => Deleted index", _delete_index)
        return True


    def create_index(self):
        es = self.es
        _es_config = ConfigElasticSearch().settings()
        _create_index = es.indices.create(body=_es_config, index=self._index, ignore=[400])
        print(f"Action => Created index", _create_index)


    def refresh_index(self):
        es = self.es
        _ref = es.indices.refresh(index=self._index)
        print(f"Action => Refreshed index", _ref)


    def add_doc(self, *, id, name, district="", country, official_name, polygon_file_name, scope):
        doc = {
            "id": id,
            "name": name,
            "official_name": official_name,
            "district": district,
            "country": country,
            "polygon_file_name": polygon_file_name,
            "scope": scope,
        }

        res = self.es.index(index=self._index, id=id, body=doc)
        print(res["result"], id, "doc: to index")

