"""
At index time use the edge_ngram

At search time use keyword (whatever user has inputed) to query elasticsearch

[see edgengram]
(https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-edgengram-tokenizer.html)
[see search-analyzer]
(https://www.elastic.co/guide/en/elasticsearch/reference/current/search-analyzer.html)
"""

class BaseConfiguration:
    """ Base class for Elastic search configuration"""
    def set(self):
        return {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "default_index_analyzer": self._index_analyzer(),
                        "default_search_analyzer": self._search_analyzer(),
                    },
                    "tokenizer": self._index_tokenizer(),
                },
            },
            "mappings": self._mappings()
        }

    def _index_analyzer(self):
        return {
            "tokenizer": "default_tokenizer",
            "filter": [
                "lowercase", "asciifolding", "apostrophe"
            ]
        }

    def _search_analyzer(self):
        return {
            "tokenizer": "keyword",
            "filter": ["lowercase", "asciifolding", "apostrophe"]
        }

    def _index_tokenizer(self):
        return {
            "default_tokenizer": {
                "type": "edge_ngram",
                "min_gram": 2,
                "max_gram": 20,
                "token_chars": [
                    "letter",
                    "digit",
                    "whitespace"
                ]
            }
        }


class PlaceConfiguration(BaseConfiguration):
    """ Configuration for Place suggestions"""

    def _mappings(self):
        return {
            "properties": {
                # uses the edge-n-gram on the name field for searching
                "name": {
                    "type": "text",
                    "analyzer": "default_index_analyzer",
                    "search_analyzer": "default_search_analyzer",
                    # name.keyword will be use for sorting and aggregation
                    # [see
                    # https://www.elastic.co/guide/en/elasticsearch/reference/current/fielddata.html]
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                # uses the search as you type field type
                # [see
                # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-as-you-type.html]
                "s_name": {
                    "type": "search_as_you_type",
                    "analyzer": "default_index_analyzer",
                    "search_analyzer": "default_search_analyzer"
                },
                "official_name": {
                    "type": "text"
                },
                "polygon_file_name": {
                    "type": "text",
                    "index": False,
                },
                "area": {
                    "type": "text",
                    "index": True,
                },
                "scope": {
                    "type": "text",
                    "index": True,
                }
            }
        }


class AmenitiesConfiguration(BaseConfiguration):
    def _mappings(self):
        return {
            "properties": {
                # uses the edge-n-gram on the name field for searching
                "amenity": {
                    "type": "text",
                    "analyzer": "default_index_analyzer",
                    "search_analyzer": "default_search_analyzer",
                    "index": True,
                },
                # school, bank, pubs
                # "category": {
                #     "type": "text",
                #     "index": True,
                # },
                # defaults to local
                "scope": {
                    "type": "text",
                    "index": False,
                }
            }
        }
