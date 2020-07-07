import json
from unittest.mock import Mock

import main


def test_scrape_fp():
    #Scrape 2 pages only
    data = {'limit': 2,'website':'fashionphile'}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    scraped_data = json.loads(main.scrape_website(req))
    
    assert len(scraped_data) > 0
    assert type(scraped_data[0]) is dict

def test_scrape_yc():
	#Scrape 2 pages only
    data = {'limit': 2,'website':'yoogicloset'}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    scraped_data = json.loads(main.scrape_website(req))
    
    assert len(scraped_data) > 0
    assert type(scraped_data[0]) is dict

def test_scrape_hewi():
	#Scrape 2 pages only
    data = {'limit': 2,'website':'hardlyeverwornit'}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    scraped_data = json.loads(main.scrape_website(req))
    
    assert len(scraped_data) > 0
    assert type(scraped_data[0]) is dict

