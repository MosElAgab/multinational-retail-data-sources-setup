import boto3
import os
import json
from dotenv import load_dotenv

# load env for local development
load_dotenv()

def lambda_handler(event, context):
    bucket_name = os.getenv("BUCKET_NAME")
    object_name = os.getenv("STORE_CSV_OBJECT_KEY")
    
    if not bucket_name or not object_name:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "missing env variables: BUCKET_NAME or TORE_CSV_OBJECT_KEY"})
        }
