from dotenv import load_dotenv
import json
import os

# load env for local development
load_dotenv()



def lambda_handler(event, context):
    bucket_name = os.getenv("BUCKET_NAME")
    object_key = os.getenv("STORE_CSV_OBJECT_KEY")
    
    if not bucket_name or not object_key:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "missing env variables: BUCKET_NAME or TORE_CSV_OBJECT_KEY"})
        }
