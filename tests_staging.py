import json
import requests
from src import params

from unittest.mock import Mock

import main

def test_endpoint():
    resp = requests.post(params.SCRAPE_ENDPOINT,json={'limit': 2,'website':'fashionphile'})
    data = json.loads(resp.content)
    print(data)
    assert -1 > 0
    assert type(data) is dict

def test_orchestrator():
    #Scrape 2 pages only
    data = {'limit': 2}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    scraped_data = json.loads(main.orchestrator(req))
    
    assert len(scraped_data) > 0
    assert type(scraped_data[0]) is dict