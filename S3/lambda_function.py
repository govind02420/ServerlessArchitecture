import boto3
from datetime import datetime, timezone, timedelta

# Set your bucket name here
BUCKET_NAME = 'my-cleanup-bucket-30days'

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    deleted_files = []

    # Get today's date
    today = datetime.now(timezone.utc)

    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            last_modified = obj['LastModified']

            # If object is older than 30 days
            if today - last_modified > timedelta(days=30):
                print(f"Deleting {key} - Last Modified: {last_modified}")
                s3.delete_object(Bucket=BUCKET_NAME, Key=key)
                deleted_files.append(key)

    return {
        'statusCode': 200,
        'deleted_files': deleted_files
    }
