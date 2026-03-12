import boto3
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def upload(local_path: str, s3_prefix: str = "raw/"):
    """
    Upload a local file to S3 bucket.
    
    Args:
        local_path: path to local file e.g. 'data/royalties.csv'
        s3_prefix:  S3 folder prefix e.g. 'raw/' or 'archive/'
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id     = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name           = os.getenv("AWS_REGION"),
    )

    bucket  = os.getenv("S3_BUCKET_NAME")
    fname   = Path(local_path).name
    s3_key  = f"{s3_prefix}{fname}"

    print(f"Uploading {local_path} → s3://{bucket}/{s3_key} ...")
    
    s3.upload_file(local_path, bucket, s3_key)
    
    print(f"✅ Done! File available at s3://{bucket}/{s3_key}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run python infra/upload_to_s3.py data/royalties.csv")
        sys.exit(1)
    
    local_file = sys.argv[1]
    prefix     = sys.argv[2] if len(sys.argv) > 2 else "raw/"
    
    upload(local_file, prefix)