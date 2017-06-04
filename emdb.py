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

    #query = {"query" : { "match" : { "_all" :  s }}, "highlight" : { "fields" : { "_all" :  {}}} }
    #query = {"query" : { "match" : { "Plot" :  s}}, "highlight" : { "fields" : { "Plot" :  {}}} }
    q = { "query": {
            "bool": {
              "should": [
                { "match": { 
                    "Title":  {
                    "query": s,
                    "boost": 2,
                    "fuzziness": 1
                }}},
                { "match": { 
                    "Director":  {
                    "query": s,
                    "boost": 2,
                    "fuzziness": 1
                }}},
                { "match": { 
                    "Plot":  {
                    "query": s,
                    "boost": 2,
                    "fuzziness": 1
                }}},
                { "match": { 
                    "Cast":  {
                    "query": s,
                    "boost": 2,
                    "fuzziness": 1
                }}},
              ]
            }
          },
          "highlight" : {
              "fields" : [
                  { "Title" : {} },
                  { "Director" : {} },
                  { "Plot" : {} },
                  { "Cast" : {} },
              ]
          }
        }
    response = es.search(index="emdb", body=q)

    h = 0
    results = {}
    for hit in response['hits']['hits']:
        results[h] = "With a " + str(hit['_score']) + " score: " + hit['_source']['Title'] + "\n"
        print hit['highlight']
        results[h] += "\tMatch highlight: .." + str(hit['highlight']) + "..\n\n"
        h = h + 1
    return jsonify(result=results, len=len(results))
    

if __name__ == "__main__":
    app.run(debug = True)
