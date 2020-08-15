import os

from src import params
from src.bigquery import run_sql_file

def run_data_pipeline():

    errors = run_sql_file(
        params.GOOGLE_CLOUD_PROJECT, 
        params.BIGQUERY_DATASET, 
        'raw_events', 
        'parsed_events', 
        os.path.join('src','sql','parse_raw_events.sql')
    )
    
    errors = run_sql_file(
        params.GOOGLE_CLOUD_PROJECT, 
        params.BIGQUERY_DATASET, 
        'parsed_events', 
        'tagged_episodes', 
        os.path.join('src','sql','tag_episodes.sql')
    )
    
    errors = run_sql_file(
        params.GOOGLE_CLOUD_PROJECT, 
        params.BIGQUERY_DATASET, 
        'tagged_episodes', 
        'latest_items', 
        os.path.join('src','sql','latest_items.sql')
    )