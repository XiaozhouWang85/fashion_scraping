import json
from flask import request

from src.parse_hardly_ever_worn import hew_fetch
from src.util import chunks
from src import params

def hello_world(request):
    request_json = request.get_json()
    if request_json and 'name' in request_json:
        name = request_json['name']
    else:
        name = 'World'
    return 'Hello, {}!\n'.format(name)

def scrape_hewi(request):
    print(type(request))
    request_json = request.get_json()
    if request_json and 'limit' in request_json:
        limit = int(request_json['limit'])
        url_list = params.HEWI_URLS[:limit]
    else:
        url_list = params.HEWI_URLS
    hew = [
        item for url_chunk in chunks(url_list,params.ASYNC_CONN_NUM) \
        for item in hew_fetch(url_chunk)
    ]
    return json.dumps(hew)
