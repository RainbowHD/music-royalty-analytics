import json
import boto3
import os
from datetime import datetime


def handler(event, context):
    """
    Triggered automatically when a new file lands in S3.
    Logs the ingestion metadata to DynamoDB for audit trail.
    """
    # Extract file details from the S3 event
    record = event['Records'][0]['s3']
    bucket = record['bucket']['name']
    key = record['object']['key']
    size = record['object']['size']

    print(f"New file detected: s3://{bucket}/{key} ({size} bytes)")

    # Log to DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
    table = dynamodb.Table('royalty_ingestion_log')

    table.put_item(Item={
        'file_key':    key,
        'bucket':      bucket,
        'file_size':   size,
        'ingested_at': datetime.now().isoformat(),
        'status':      'PENDING_SNOWFLAKE_LOAD'
    })

    return {
        'statusCode': 200,
        'body': json.dumps({'file': key, 'status': 'logged'})
    }