import os

ENV_PROJECT = os.environ['GCLOUD_PROJECT']

#Google cloud settings
if ENV_PROJECT == 'prod':
	GOOGLE_CLOUD_PROJECT = 'fashion-scraping'
elif ENV_PROJECT == 'staging':
	GOOGLE_CLOUD_PROJECT = 'fashion-scraping-staging'

BIGQUERY_DATASET = 'prod'
BIGQUERY_TABLE = 'raw_events'


#Number of connections to set up when scraping asynchronously
ASYNC_CONN_NUM = 10

#Endpoints for deployed scraping functions
SCRAPE_HEWI_ENDPOINT = "https://us-central1-fashion-scraping.cloudfunctions.net/scrape_website"
