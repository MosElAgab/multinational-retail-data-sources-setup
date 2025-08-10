from dotenv import load_dotenv
import json
import os
import boto3
import csv
import io

# load env for local development
load_dotenv()

def get_store_data(bucket_name, object_key):
    # should retrun list of dictionaries given csv file
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    content = response['Body'].read().decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(content))
    data = list(csv_reader)
    return data

def get_store_by_row_index(bucket_name, object_key, index):
    data = get_store_data(bucket_name, object_key)

    return data[index]

def lambda_handler(event, context):
    bucket_name = os.getenv("BUCKET_NAME")
    object_key = os.getenv("STORE_CSV_OBJECT_KEY")
    
    if not bucket_name or not object_key:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "missing env variables: BUCKET_NAME or STORE_CSV_OBJECT_KEY"})
        }
    

