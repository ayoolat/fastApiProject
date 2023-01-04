import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile

s3 = boto3.client("s3")


def upload_to_aws(local_file: str, s3_file: str):
    try:
        print(local_file)
        print(s3_file)

        s3.put_object(
            Bucket='cake-shop-1234',
            Key=s3_file,
            Body=local_file,
            ContentType='image/jpeg',
            ACL='public-read'
        )
        return s3_file
    except FileNotFoundError as e:
        raise e
    except NoCredentialsError as e:
       raise e
