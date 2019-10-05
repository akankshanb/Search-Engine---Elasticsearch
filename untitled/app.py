from flask import Flask
from flask import render_template, redirect, request, url_for, Response
from forms import SubmitSearchForm
from elasticsearch import Elasticsearch
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-key-here'
es_conn = Elasticsearch('localhost:9200')

def more_like_this_query(field,keywords):
    query = {
        "query": {
            "more_like_this": {
                "fields": [
                    field
                ],
                "like": keywords,
                "min_term_freq": 1,
                "max_query_terms": 20
            }
        }
    }
    response = es_conn.search(index='bills', body=query)
    if response.get('hits', {}).get('total', {}).get('value', 0) > 0:
        return response['hits']['total']['value'], response['hits']['hits']
    else:
        return 0,None

def filter_match_query(field,keywords,kw):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {field: keywords}}
                ],
                "filter": [
                    {"term": {"Category": kw}}
                ]
            }
        }
    }
    response = es_conn.search(index='bills', body=query)
    if response.get('hits', {}).get('total', {}).get('value', 0) > 0:
        return response['hits']['total']['value'], response['hits']['hits']
    else:
        return 0,None

def filter_mlt_query(field,keywords,kw):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"more_like_this": {
                        "fields": [
                            field
                        ],
                        "like": keywords,
                        "min_term_freq": 1,
                        "max_query_terms": 20
                        }
                    }
                ],
                "filter": [
                    {"term": {"Category": kw}}
                ]
            }
        }
    }
    response = es_conn.search(index='bills', body=query)
    if response.get('hits', {}).get('total', {}).get('value', 0) > 0:
        return response['hits']['total']['value'], response['hits']['hits']
    else:
        return 0,None

def match_query(field,keyword):
   query={"query":{"match":{field:keyword}}}
   response = es_conn.search(index= 'bills', body = query)
   if response.get('hits', {}).get('total', {}).get('value',0) > 0:
       return response['hits']['total']['value'], response['hits']['hits']
   else:
       return 0, None

def match_query_with_AND_operator(keyword):
   query={"query":{"match" : { "text":{"query":keyword,"operator":"and"}}}}
   response = es_conn.search(index= 'bills', body = query)
   if response.get('hits', {}).get('total', {}).get('value',0) > 0:
       return response['hits']['hits'][0]['_source']['text']
   else:
       return 0, None

@app.route('/')
def index():
    form =SubmitSearchForm()
    return render_template(
        'index.html',form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
    keyword_map = {'op': 'Operations',
                   'gg': 'General Government',
                   'ed': 'Education',
                   'fi': 'Finance',
                   'hl': 'Health',
                   'tr': 'Transportation',
                   'ag': 'Agriculture',
                   'en': 'Environment'
                   }
    if request.method == "POST":
        key = request.form["key"]
        keyword = request.form["keywords"]
        query = request.form["repo_url"]
        num_hits=0
        hits=None
        if query and query!= "":
            if keyword == "none":
                if key == "bid":
                    num_hits, hits = match_query("bill_id",query)
                elif key == "bs":
                    num_hits, hits = more_like_this_query("bill_sponsors", query)
                elif key == "txt":
                    num_hits, hits = more_like_this_query("clean_data", query)
            else:
                kw = keyword_map[keyword]
                if key == "bid":
                    num_hits, hits = filter_match_query("bill_id",query,kw)
                elif key == "bs":
                    num_hits, hits = filter_mlt_query("bill_sponsors", query,kw)
                elif key == "txt":
                    num_hits, hits = filter_mlt_query("clean_data", query,kw)
        return render_template('process.html',num_hits=num_hits,hits=hits,form=SubmitSearchForm())

    return render_template('results.html',num_hits=0,hits=None)

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method=="POST":
        print(request)
    else:
        print("no")
    return render_template('process.html')


if __name__ == '__main__':
    app.run()
