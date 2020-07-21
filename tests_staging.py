import json
import requests
from src import params
from src.bigquery import reset_logged_data
from unittest.mock import Mock

import main

def test_staging_data_reset():
    errors = reset_logged_data()
    
    assert len(errors) == 0

def test_endpoint():

    errors = reset_logged_data()

    resp = requests.post(params.SCRAPE_ENDPOINT,json={'limit': 2,'website':'fashionphile'})
    data = json.loads(resp.content)
    
    assert len(data) > 0
    assert type(data[0]) is dict

def test_orchestrator_local():
    errors = reset_logged_data()

    #Scrape 2 pages only
    data = {"limit": 2}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function

    scraped_data = json.loads(main.orchestrator(req))
    
    assert len(scraped_data) > 0
    assert type(scraped_data[0]) is dict

def test_orchestrator_staging():
    errors = reset_logged_data()

    resp = requests.post(params.ORCHESTRATOR_ENDPOINT,json={'limit': 2})
    data = json.loads(resp.content)
    
    assert len(data) > 0
    assert type(data[0]) is dict