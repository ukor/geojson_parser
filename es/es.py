"""
Interface for elastic search
"""
import simplejson as json
# from .es_config import ConfigElasticSearch
# from config.config import ES_INDEX_NAME

class es_client:
    def __init__(self, es_instance, es_index=None):
        self.es = es_instance;
        self._index = "homeknock_places" if es_index in [None, False, "", 0] else es_index


    def delete_index(self):
        """delete_index This method will delete the entire index,
                        This action can not be undone - use with caution

        Returns:
            bool: Returns True after delete operation
        """
        es = self.es
        _delete_index = es.indices.delete(index=self._index, ignore=[400])
        print(f"Action => Deleted index", _delete_index)
        return True


    def create_index(self, *, configuration_instance):
        es = self.es
        _create_index = es.indices.create(
            body=configuration_instance().set(),
            index=self._index, ignore=[400]
        )
        print(f"Action => Created index", _create_index)


    def refresh_index(self):
        es = self.es
        _ref = es.indices.refresh(index=self._index)
        print(f"Action => Refreshed index", _ref)


    def delete_by_query(self, query_string):
        """delete_by_query Deletes documents that match the query_string

        Args:
            query_string (str): String document is matched against
        """
        es = self.es
        query = {
            "query": {
                "match": {
                    "id": query_string
                }
            }
        }
        _delete_index = es.delete_by_query(index=self._index, ignore=[400], body=query)
        print(f"Action => Deleted document with scope = {query_string}", _delete_index)


    def add_doc(self, *, id, name, area, official_name, polygon_file_name, scope):
        doc = {
            "id": id,
            "name": name,
            # field for search-as-you-type
            "s_name": name,
            "official_name": official_name,
            "area": area,
            "polygon_file_name": polygon_file_name,
            "scope": scope,
        }

        res = self.es.index(index=self._index, id=id, body=doc)
        print(res["result"], id, "doc: to index")

    def add_document(self, document: dict):
        res = self.es.index(index=self._index, id=document.get('id', None), body=document)
        print(res, "doc: to index")
        return res

