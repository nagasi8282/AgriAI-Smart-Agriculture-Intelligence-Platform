"""
AgriAI Storage Layer - AWS S3 Cloud Storage Provider
Manages object storage in AWS S3 for the cloud Medallion Data Lake.
Falls back gracefully when cloud credentials are not supplied.
"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Any
from backend.config.settings import settings

logger = logging.getLogger(__name__)


class S3StorageProvider:
    """Manages cloud object storage in AWS S3 with least-privilege access patterns."""

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        region: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        self.bucket_name = bucket_name or settings.S3_BUCKET_NAME
        self.region = region or settings.AWS_REGION
        self.aws_access_key_id = aws_access_key_id or settings.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = aws_secret_access_key or settings.AWS_SECRET_ACCESS_KEY
        self.is_configured = bool(self.aws_access_key_id and self.aws_secret_access_key and self.bucket_name)

        if not self.is_configured:
            logger.info("AWS S3 credentials not provided. S3StorageProvider running in unconfigured fallback mode.")

    def upload_file(self, local_path: Path, s3_key: str) -> bool:
        """Upload a local file to S3 bucket key."""
        if not self.is_configured:
            logger.warning(f"S3 upload skipped: AWS credentials not configured. Target key: {s3_key}")
            return False

        try:
            import boto3
            from botocore.exceptions import ClientError

            s3_client = boto3.client(
                "s3",
                region_name=self.region,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            )
            s3_client.upload_file(str(local_path), self.bucket_name, s3_key)
            logger.info(f"Successfully uploaded {local_path} to s3://{self.bucket_name}/{s3_key}")
            return True
        except Exception as e:
            logger.error(f"Failed to upload to S3: {e}")
            return False

    def download_file(self, s3_key: str, local_path: Path) -> bool:
        """Download an S3 object to local filesystem."""
        if not self.is_configured:
            logger.warning(f"S3 download skipped: AWS credentials not configured. Key: {s3_key}")
            return False

        try:
            import boto3

            s3_client = boto3.client(
                "s3",
                region_name=self.region,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            )
            local_path.parent.mkdir(parents=True, exist_ok=True)
            s3_client.download_file(self.bucket_name, s3_key, str(local_path))
            return True
        except Exception as e:
            logger.error(f"Failed to download from S3: {e}")
            return False


s3_storage = S3StorageProvider()
