import os
import json
import requests
from src import params
from src.bigquery import reset_logged_data, run_sql_file
from src.bigquery import get_item_data
from src.firestore import insert_to_firestore

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

def test_bigquery_download():
    df_json = get_item_data(project_id="fashion-scraping")

    assert type(df_json[0]) is dict

def test_firetore_upload():

    json_list = [
        {'name': 'New York City', 'city_code':"NYC"},
        {'name': 'San Francisco', 'city_code':"SF"}
    ]
    key_field = 'city_code'

    collection = 'cities'
    
    insert_to_firestore(json_list,key_field,collection)


def test_bigquery_to_firestore():

    json_list = get_item_data(project_id="fashion-scraping")
    key_field = 'item_ID'

    collection = 'item_data'
    
    insert_to_firestore(json_list,key_field,collection)