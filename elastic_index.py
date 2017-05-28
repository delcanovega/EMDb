# This script indexes our MongoDB collection
# with the ElasticSearch engine in order to
# perform more optimal searches

from elasticsearch import Elasticsearch
from humbledb import Mongo, Document

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

class MovieDoc(Document):
    config_database = 'emdb'
    config_collection = 'movies'

with Mongo:
    for m in MovieDoc.find():
        content = m.for_json()
        content.pop('_id', None)
        es.index(index='emdb', doc_type='movie', id=m['_id'], body=content)
