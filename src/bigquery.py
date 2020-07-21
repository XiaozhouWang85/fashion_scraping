from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from datetime import datetime
import json

from src import params

BIGQUERY_RAW_EVENTS_SCHEMA = [
    bigquery.SchemaField("website", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("insertion_timestamp", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("payload", "STRING", mode="REQUIRED"),
]

def create_table_if_not_exist(project_id, dataset_id, table_id):
    client = bigquery.Client(project_id)
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    table_ref = dataset_ref.table(table_id)
    try:
        table = client.get_table(table_ref)

    except NotFound as error:
        table = bigquery.Table(table_ref, schema = BIGQUERY_RAW_EVENTS_SCHEMA)
        client.create_table(table)

    return client, table

def empty_table(project_id, dataset_id, table_id):
    client = bigquery.Client(project_id)
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    table_ref = dataset_ref.table(table_id)
    
    job_config = bigquery.QueryJobConfig()
    job_config.destination = dataset_ref.table(table_id)
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

    sql = """
        SELECT * 
        FROM `{}`.`{}`.`{}` LIMIT 0;
    """.format(project_id, dataset_id, table_id)
    
    query_job = client.query(sql,location='US',job_config=job_config)

    return list(query_job.result())

def log_to_bigquery(json_payloads):

    client, table = create_table_if_not_exist(params.GOOGLE_CLOUD_PROJECT, params.BIGQUERY_DATASET, params.BIGQUERY_TABLE)

    data_row = [
        parse_payload(payload) for payload in json_payloads
    ]
    errors = client.insert_rows(table, data_row)
    return errors

def reset_logged_data():

    errors = empty_table(params.GOOGLE_CLOUD_PROJECT, params.BIGQUERY_DATASET, params.BIGQUERY_TABLE)

    return errors

def parse_payload(payload):
    payload_str = json.dumps(payload)
    site = payload['site']
    
    return (site, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), payload_str)