import json
from flask import request

from src.parse_hardly_ever_worn import hewi_fetch
from src.parse_yoogis_closet import yc_fetch

from src import params

def hello_world(request):
    request_json = request.get_json()
    if request_json and 'name' in request_json:
        name = request_json['name']
    else:
        name = 'World'
    return 'Hello, {}!\n'.format(name)

def scrape_hewi(request):
    request_json = request.get_json()
    if request_json and 'limit' in request_json:
        limit = int(request_json['limit'])
    else:
        limit = None
    hewi = hewi_fetch(limit)
    return json.dumps(hewi)

def scrape_yc(request):
    request_json = request.get_json()
    if request_json and 'limit' in request_json:
        limit = int(request_json['limit'])
    else:
        limit = None
    yc = yc_fetch(limit)
    return json.dumps(yc)
