import os

GOOGLE_CLOUD_PROJECT = os.environ['GCLOUD_PROJECT']

BIGQUERY_DATASET = 'prod'
BIGQUERY_TABLE = 'raw_events'


#Number of connections to set up when scraping asynchronously
ASYNC_CONN_NUM = 10

#Endpoints for deployed scraping functions
if GOOGLE_CLOUD_PROJECT == 'fashion-scraping':
    SCRAPE_ENDPOINT = "https://us-central1-fashion-scraping.cloudfunctions.net/scrape_website"
elif GOOGLE_CLOUD_PROJECT == 'fashion-scraping-staging':
    SCRAPE_ENDPOINT = "https://us-central1-fashion-scraping-staging.cloudfunctions.net/scrape_website"
else:
    SCRAPE_ENDPOINT = "https://us-central1-fashion-scraping-staging.cloudfunctions.net/scrape_website"

SITES = [
    "hardlyeverwornit",
    "yoogiscloset",
    "fashionphile"
]