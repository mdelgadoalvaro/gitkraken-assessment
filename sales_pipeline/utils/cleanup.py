import os
import glob
from sales_pipeline.utils.logger import get_logger
from sales_pipeline.utils.constants import CLEANED_CSV, REPORT_FOLDER

logger = get_logger("cleanup")


def clean_generated_files() -> None:
    logger.info("Cleaning generated output files...")

    files_to_remove = (
        glob.glob(CLEANED_CSV) +
        glob.glob(f"{REPORT_FOLDER}/*.png") +
        glob.glob(f"{REPORT_FOLDER}/*.pdf")
    )

    for file_path in files_to_remove:
        try:
            os.remove(file_path)
            logger.info(f"Deleted: {file_path}")
        except Exception as error:
            logger.warning(f"Could not delete {file_path}: {error}")


if __name__ == '__main__':
    clean_generated_files()
