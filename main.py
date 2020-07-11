import json
from flask import request

from src.parse_hardly_ever_worn import hewi_fetch
from src.parse_yoogis_closet import yc_fetch
from src.parse_fashion_phile import fp_fetch
from src import params

def orchestrator(request):
    request_json = request.get_json()
    if request_json and 'name' in request_json:
        name = request_json['name']
    else:
        name = 'World'
    return 'Hello, {}!\n'.format(name)


def scrape_website(request):
    request_json = request.get_json()

    if request_json and 'website' in request_json:
        website = request_json['website']
    else:
        raise ValueError('Website was not specified on payload')

    if request_json and 'limit' in request_json:
        limit = int(request_json['limit'])
    else:
        limit = None

    if website == "hardlyeverwornit":
        scraped_data = hewi_fetch(limit)
    elif website == "yoogicloset":
        scraped_data = yc_fetch(limit)
    elif website == "fashionphile":
        scraped_data = fp_fetch(limit)        

    return json.dumps(scraped_data)
