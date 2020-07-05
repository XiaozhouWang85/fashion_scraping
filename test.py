import json
from unittest.mock import Mock

import main

def test_scrape_hewi():
	#Scrape 2 pages only
    data = {'limit': 2}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    scraped_data = json.loads(main.scrape_hewi(req))
    
    assert len(scraped_data) > 0
    assert type(scraped_data[0]) is dict