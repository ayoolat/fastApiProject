import boto3
from botocore.exceptions import NoCredentialsError

s3 = boto3.resource("s3")

for bucket in s3.buckets.all():
    print(bucket.name)


def upload_to_aws(local_file, s3_file):
    try:
        upload = s3.upload_file(local_file, "cake-shop-1234", s3_file)
        print("Upload Successful")
        return upload
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False