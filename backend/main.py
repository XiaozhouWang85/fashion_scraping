import json
from flask import request

from src.parse_hardly_ever_worn import hewi_fetch
from src.parse_yoogis_closet import yc_fetch
from src.parse_fashion_phile import fp_fetch
from src.bigquery import log_to_bigquery
from src.data_pipeline import run_data_pipeline
from src.util import async_post, get_gcp_logger

from src import params

def orchestrator(request):
    logger = get_gcp_logger()
    request_json = request.get_json()

    num_sites = len(params.SITES)
    url = [params.SCRAPE_ENDPOINT]*num_sites

    log_message = {}
    log_message.update({
        "Process":"Orchestrator",
        "Process Start":"Orchestrator - Starting scrapers ⏱"
    })

    if request_json and 'limit' in request_json:
        payloads = [{"website":site,"limit": int(request_json['limit'])} for site in params.SITES]
    else:
        payloads = [{"website":site} for site in params.SITES]
    
    try:
    
        data = [
            content for resp_contents in async_post(url,payloads) \
            for content in json.loads(resp_contents)
        ]

        
        run_data_pipeline()

        log_message.update({
            "Process":"Orchestrator",
            "Process End":"Orchestrator - Pipeline finished 🏁"
        })

        logger.log_struct(log_message, 'INFO')

        return json.dumps(data[:3])
    
    except Exception as e:
        log_message.update({
            "Process End": str(e)
        })
        logger.log_struct(log_message, 'ERROR')


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
    elif website == "yoogiscloset":
        scraped_data = yc_fetch(limit)
    elif website == "fashionphile":
        scraped_data = fp_fetch(limit)

    if request_json and 'log_to_bigquery' in request_json:
        if request_json['log_to_bigquery'] == False:
            pass
        else:
            log_to_bigquery(scraped_data)
    else:
        log_to_bigquery(scraped_data)

    return json.dumps(scraped_data[:3])
