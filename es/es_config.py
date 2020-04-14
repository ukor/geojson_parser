"""
At index time use the edge_ngram

At search time use whatever th user as input to query elasticsearch

[see edgengram](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-edgengram-tokenizer.html)
[see search-analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-analyzer.html)
"""


class ConfigElasticSearch:

    def settings(self):
        return {
            "settings": {
                "analysis": {
                    "filter": self._index_filter(),
                    "analyzer": {
                        "index_place": self._index_analyzer(),
                        "search_place": self._search_analyzer(),
                    },
                    "tokenizer": self._index_tokenizer(),
                },
            },
            "mappings": self._mappings()
        }


    def _index_filter(self):
        return {
            "place_filter": {
                "type": "edge_ngram",
                "min_gram": 1,
                "max_gram": 20,
            }
        }


    def _index_tokenizer(self):
        return {
            "place_tokenizer": {
                "type": "edge_ngram",
                "min_gram": 2,
                "max_gram": 10,
                "token_chars": [
                    "letter",
                    "digit",
                ]
            }
        }


    def _index_analyzer(self):
        return {
            "type": "custom",
            "tokenizer": "place_tokenizer",
            "filter": [
                "lowercase", "asciifolding", "apostrophe", "place_filter"
            ]
        }


    def _search_analyzer(self):
        return {
            "tokenizer": "keyword",
            "filter": ["lowercase", "asciifolding", "apostrophe"]
        }


    def _mappings(self):
        return {
            "properties": {
                "name": {
                    "type": "text",
                    "analyzer": "index_place",
                    "search_analyzer": "search_place"
                },
                "official_name": {
                    "type": "text"
                },
                "geo_path": {
                    "type": "text",
                    "index": False,
                },
                "scope": {
                    "type": "text",
                    "index": False,
                }
            }
        }

