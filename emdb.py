from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@app.route("/")
def index():
    return render_template("index_form.html")

@app.route("/search")
def search():
    s = request.args.get('s')
    query = {"query" : { "fuzzy" : { "_all" : { "value" : s }}} }
    response = es.search(index="emdb", body=query)
    h = 0
    results = {}
    for hit in response['hits']['hits']:
        results[h] = "With a " + str(hit['_score']) + " score: " + hit['_source']['Title']
        #results[h] += "Match highlight: " + hit['_highlight']
        h = h + 1
    return jsonify(result=results, len=len(results))

if __name__ == "__main__":
    app.run(debug = True)
