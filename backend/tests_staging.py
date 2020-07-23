import os
import json
import requests
from src import params
from src.bigquery import reset_logged_data, run_sql_file
from unittest.mock import Mock

import main

def test_staging_data_reset():
    errors = reset_logged_data()
    
    assert errors is None

def test_sql():

    errors = run_sql_file(
        'fashion-scraping-staging', 
        'prod', 
        'raw_events', 
        'parsed_events', 
        os.path.join('src','sql','parse_raw_events.sql')
    )

    errors = run_sql_file(
        'fashion-scraping-staging', 
        'prod', 
        'parsed_events', 
        'tagged_episodes', 
        os.path.join('src','sql','tag_episodes.sql')
    )
    
    errors = run_sql_file(
        'fashion-scraping-staging', 
        'prod', 
        'tagged_episodes', 
        'latest_items', 
        os.path.join('src','sql','latest_items.sql')
    )

    assert errors is None

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
