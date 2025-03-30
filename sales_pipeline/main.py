import os
import sys
from sales_pipeline.ingest import ingest_csvs
from sales_pipeline.process import process_data
from sales_pipeline.analyze import generate_charts_and_report
from sales_pipeline.upload_to_s3 import upload_to_s3
from sales_pipeline.utils.envs import get_bool_env
from sales_pipeline.utils.logger import get_logger
from sales_pipeline.utils.cleanup import clean_generated_files
from sales_pipeline.utils.constants import CLEANED_CSV, REPORT_PDF, DATA_FOLDER

logger = get_logger("main")

aws_upload = get_bool_env("AWS_UPLOAD")
bucket = os.environ.get("AWS_S3_BUCKET")
clean_output = get_bool_env("CLEAN_OUTPUT", "false")


def main():
    logger.info("Ingesting CSV files...")
    raw_df = ingest_csvs(DATA_FOLDER)

    logger.info("Cleaning and processing data...")
    cleaned_df = process_data(raw_df)

    logger.info("Analyzing and generating charts/report...")
    generate_charts_and_report(cleaned_df)

    if aws_upload:
        logger.info("Uploading cleaned data and report to S3...")
        uploads = {
            CLEANED_CSV: f"data/{CLEANED_CSV}",
            REPORT_PDF: f"reports/{os.path.basename(REPORT_PDF)}"
        }
        if not bucket:
            logger.error("Missing required environment variable: AWS_S3_BUCKET")
        else:
            for local_file, s3_key in uploads.items():
                if os.path.exists(local_file):
                    upload_to_s3(local_file, bucket, s3_key)
                else:
                    logger.error(f"File not found: {local_file}")

    if clean_output:
        clean_generated_files()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        logger.exception("Pipeline failed with an error: ", error)
        sys.exit(1)
