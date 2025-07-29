import boto3
import json
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import requests

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
            # s3_client = boto3.client('s3')
            s3_client = boto3.client('s3', region_name="eu-west-2")
        except ClientError as e:
            print(e)
            return False
    else:
        try:
            session = boto3.Session(profile_name=aws_cli_profile)
            # s3_client = session.client("s3")
            s3_client = session.client("s3", region_name="eu-west-2")
        except ClientError as e:
            print(e)
            return False
    
    # upload object
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print("file uploaded")
    except ClientError as e:
        print(e)
        return False
    return True





def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    # s3_client = boto3.client('s3')
    # s3_client = boto3.client('s3', region_name="eu-west-2")
    session = boto3.Session(profile_name="mos")
    s3_client = session.client("s3", region_name="eu-west-2")
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        print(e)
        return None

    # The response contains the presigned URL
    return response

# --- Config ---
bucket_name = "data-handling-public-moselagab"
region = "eu-west-2"
object_key = "card_details.pdf"
file_name = "data/card_details.pdf"
aws_cli_profile=os.getenv("AWS_CLI_PROFILE")

create_bucket(bucket_name, region, aws_cli_profile)
upload_file(file_name, bucket_name, aws_cli_profile=aws_cli_profile)

object_name = os.path.basename(file_name)
url = create_presigned_url(bucket_name,object_name)
print(url)

# FIXME: pre-signed url not workign, gives 403 forbidden
response = requests.get(url)
print(response.status_code)
print(response.json)