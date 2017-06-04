# EMDb
EMDb is a small contact take with ElasticSearch and the AJAX technology for real time searching.
### Files
* **mongo_loader.py:** This script uses the IMDbPy API to load 250 movies into a MongoDB database.
* **elastic_index.py:** This other script takes our MongoDB collection and indexes it in order to use ElasticSearch as our search engine.
* **emdb.py:** Our webapp developed with Flask
