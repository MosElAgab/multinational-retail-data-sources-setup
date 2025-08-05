import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import requests

# loads .en environment variables
load_dotenv()

# utils
#TODO: remove create bucket, not needed anymore
def create_bucket(
        bucket_name: str,
        region: str = "us-east-1",
        aws_cli_profile: str = None
):
    """
    Create an S3 bucket in the specified region using an optional AWS CLI profile.

    Args:
        bucket_name (str): Name of the S3 bucket to create.
        region (str): AWS region where the bucket will be created.
        aws_cli_profile (str, optional): Named AWS CLI profile to use. Defaults to None.

    Returns:
        bool: True if bucket creation succeeds or already exists; False on error.
    """

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


def upload_file(
        file_name: str,
        bucket: str,
        object_name: str = None,
        aws_cli_profile: str = None
):
    """
    Upload a file to an S3 bucket.

    Args:
        file_name (str): Local path to the file.
        bucket (str): Target S3 bucket name.
        object_name (str, optional): Key (name) to assign in S3. Defaults to file basename.
        aws_cli_profile (str, optional): Named AWS CLI profile. Defaults to None.

    Returns:
        bool: True if upload succeeds, False otherwise.
    """

    object_name = object_name or os.path.basename(file_name)

    # TODO: check if need region but i guess we dont need it since bucket name is unique
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
    Generate a presigned GET URL for an S3 object.

    Args:
        expires_in (int): Expiration time in seconds.
        region (str): AWS region of the bucket.
        bucket_name (str): S3 bucket name.
        object_name (str): Key of the object to generate the URL for.
        aws_cli_profile (str, optional): Named AWS CLI profile. Defaults to None which uses default aws cli profile.

    Returns:
        str: Presigned URL as a string if successful, None otherwise.
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


def main():
    # # --- Config/Params ---
    bucket_name = "data-handling-public-moselagab"
    region = "eu-west-2"
    file_name = "data/card_details.pdf"
    aws_cli_profile=os.getenv("AWS_CLI_PROFILE")
    object_name = os.path.basename(file_name)
    expires_in=3600 * 24 * 7 # 7 day

    # create_bucket(bucket_name, region, aws_cli_profile)
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

if __name__ == "__main__":
    main()
