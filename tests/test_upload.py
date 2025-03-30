from unittest.mock import patch
from sales_pipeline.utils.upload_to_s3 import upload_to_s3


@patch("boto3.client")
def test_upload_to_s3_success(mock_boto):
    mock_s3 = mock_boto.return_value
    upload_to_s3("fake_file.csv", "test-bucket", "data/fake.csv")
    mock_s3.upload_file.assert_called_once_with("fake_file.csv", "test-bucket", "data/fake.csv")
