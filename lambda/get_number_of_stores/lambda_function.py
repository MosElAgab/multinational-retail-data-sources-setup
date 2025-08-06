import boto3
import os
import json
import csv
import io
from dotenv import load_dotenv

# load env for local development
load_dotenv()


def count_number_of_stores(bucket_name, object_key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    content = response['Body'].read().decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(content))
    count = len(list(csv_reader))
    return count


def lambda_handler(event, context):
    bucket_name = os.getenv("BUCKET_NAME")
    object_key = os.getenv("STORE_CSV_OBJECT_KEY")
    
    if not bucket_name or not object_key:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "missing env variables: BUCKET_NAME or TORE_CSV_OBJECT_KEY"})
        }
    
    try:
        count = count_number_of_stores(bucket_name, object_key)
        return {
            "statusCode": 200,
            "body": json.dumps({"number_stores": count})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
