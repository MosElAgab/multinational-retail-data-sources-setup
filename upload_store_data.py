import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv


# loads .en environment variables
load_dotenv()

# utils

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

def main():
    # # --- Config/Params ---
    bucket_name = "data-handling-public-moselagab"
    file_name = "data/legacy_store_details.csv"
    aws_cli_profile=os.getenv("AWS_CLI_PROFILE")

    upload_file(file_name, bucket_name, aws_cli_profile=aws_cli_profile)

if __name__ == "__main__":
    main()