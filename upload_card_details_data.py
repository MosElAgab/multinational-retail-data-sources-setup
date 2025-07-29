import boto3
import json
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

# loads .en environment variables
load_dotenv()

# utils
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


def upload_file(file_name, bucket, object_name=None, aws_cli_profile=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

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
    
    # upload object
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True


# --- Config ---
bucket_name = "data-handling-public-moselagab"
region = "eu-west-2"
object_key = "card_details.pdf"
file_name = "data/card_details.pdf"
aws_cli_profile=os.getenv("AWS_CLI_PROFILE")

create_bucket(bucket_name, region, aws_cli_profile)
upload_file(file_name, bucket_name, aws_cli_profile=aws_cli_profile)

