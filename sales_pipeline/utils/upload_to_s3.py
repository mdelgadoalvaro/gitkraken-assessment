import boto3
from sales_pipeline.utils.logger import get_logger

logger = get_logger("uploader")


def upload_to_s3(local_file_path: str, bucket_name: str, s3_path: str) -> None:
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_file_path, bucket_name, s3_path)
        logger.info(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_path}")
    except Exception as error:
        logger.error(f"Failed to upload {local_file_path}: {error}")
