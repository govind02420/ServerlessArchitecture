import boto3
from datetime import datetime, timezone, timedelta

BUCKET_NAME = 'log-cleanup-bucket-b1'  # Replace with your actual bucket

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    retention_period = 90
    deleted_logs = []

    # Get the current time
    now = datetime.now(timezone.utc)

    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            last_modified = obj['LastModified']

            age = (now - last_modified).days
            if age > retention_period:
                print(f"Deleting: {key} (Age: {age} days)")
                s3.delete_object(Bucket=BUCKET_NAME, Key=key)
                deleted_logs.append(key)

    return {
        'statusCode': 200,
        'deleted_logs': deleted_logs
    }
