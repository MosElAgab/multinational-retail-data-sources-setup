import boto3
import json
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

# --- Config ---
bucket_name = "data-handling-public-moselagab"
region = "eu-west-2"
object_key = "card_details.pdf"
file_name = "data/card_details.pdf"


def create_bucket(bucket_name, region="us-east-1", aws_cli_profile=None):
    # configuring aws cli profile
    if aws_cli_profile is None:
        try:
            s3_client = boto3.client('s3', region_name=region)
        except ClientError as e:
            print(e)
            return False
    else:
        try:
            session = boto3.Session(profile_name=aws_cli_profile)
            s3_client = session.client("s3", region_name=region)
        except ClientError as e:
            print(e)
            return False
    # creating bucket
    try:
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print("Bucket created!")
    except ClientError as e:
        print(e)
        return False
    return True

create_bucket(bucket_name, region)

