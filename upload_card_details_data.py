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
    # CEHCK: we dont need region since bucket name is unique
    if object_name is None:
        object_name = os.path.basename(file_name)

    # configuring aws cli profile
    if aws_cli_profile is None:
        try:
            s3_client = boto3.client('s3')
        except ClientError as e:
            print(e)
            return False
    else:
        try:
            session = boto3.Session(profile_name=aws_cli_profile)
            s3_client = session.client("s3")
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


def generate_presigned_get_url(
        expires_in: int,
        region: str,
        bucket_name: str,
        object_name: str,
        aws_cli_profile: str = None
):
    """
    Generate a presigned Amazon S3 Get URL that can be used to perform an action.
    
    :param expires_in: The number of seconds the presigned URL is valid for.
    :param client_method: The name of the client method that the URL performs.
    :param method_parameters: The parameters of the specified client method.
    :return: The presigned URL.
    """
    client_method="get_object"

    # configuring aws cli profile
    if aws_cli_profile is None:
        try:
            s3_client = boto3.client('s3', region_name=region)
        except ClientError as e:
            print(e)
            return None
    else:
        try:
            session = boto3.Session(profile_name=aws_cli_profile)
            s3_client = session.client("s3", region_name=region)
        except ClientError as e:
            print(e)
            return None

    method_parameters = {"Bucket": bucket_name, "Key": object_name}
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method,
            Params=method_parameters,
            ExpiresIn=expires_in
        )
    except ClientError:
        print(f"Couldn't get a presigned URL for client method '{client_method}'.")
        raise
    print("url:")
    print(url)
    return url


# # --- Config/Params ---
bucket_name = "data-handling-public-moselagab"
region = "eu-west-2"
file_name = "data/card_details.pdf"
aws_cli_profile=os.getenv("AWS_CLI_PROFILE")
object_name = os.path.basename(file_name)
expires_in=3600 * 24 * 7 # 7 day

create_bucket(bucket_name, region, aws_cli_profile)
upload_file(file_name, bucket_name, aws_cli_profile=aws_cli_profile)

url = generate_presigned_get_url(
    expires_in=expires_in,
    aws_cli_profile=aws_cli_profile,
    region=region,
    bucket_name=bucket_name,
    object_name=object_name
)


# check url
response = requests.get(url)
if response.ok:
    print(f"URL working; response_status: {response.status_code}, file_type: {response.headers['Content-Type']}")
else:
    print(f"URL NOT working; response_status: {response.status_code}, body: {response.json}")
