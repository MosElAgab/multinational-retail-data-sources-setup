import boto3
import json
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import requests

# --- Config ---
bucket_name = "data-handling-public-moselagab"
region = "eu-west-2"
object_key = "card_details.pdf"
file_name = "data/card_details.pdf"
aws_cli_profile=os.getenv("AWS_CLI_PROFILE")

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
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

# object_name = os.path.basename(file_name)
# url = create_presigned_url(bucket_name,object_name)
# print(url)

# # FIXME: pre-signed url not workign, gives 403 forbidden
# response = requests.get(url)
# print(response.status_code)
# print(response.json)



###################################################################################################
def generate_presigned_url(s3_client, client_method, method_parameters, expires_in):
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.
    
    :param s3_client: A Boto3 Amazon S3 client.
    :param client_method: The name of the client method that the URL performs.
    :param method_parameters: The parameters of the specified client method.
    :param expires_in: The number of seconds the presigned URL is valid for.
    :return: The presigned URL.
    """
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method,
            Params=method_parameters,
            ExpiresIn=expires_in
        )
    except ClientError:
        print(f"Couldn't get a presigned URL for client method '{client_method}'.")
        raise
    return url

def main(bucket_name, object_name):
    # By default, this will use credentials from ~/.aws/credentials
    # s3_client = boto3.client("s3")
    session = boto3.Session(profile_name="mos")
    s3_client = session.client("s3", region_name="eu-west-2")
    
    # The presigned URL is specified to expire in 1000 seconds
    url = generate_presigned_url(
        s3_client, 
        "get_object", 
        {"Bucket": bucket_name, "Key": object_name}, 
        3600
    )
    print(f"Generated GET presigned URL: {url}")
    return url


object_name = os.path.basename(file_name) 
url = main(bucket_name, object_name)
print(url)

response = requests.get(url)
print(response.status_code)
print(response.json)
