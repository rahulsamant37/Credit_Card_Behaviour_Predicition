import gdown
from src import logger
from pathlib import Path
from src.entity.config_entity import (DataIngestionConfig)

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_files(self):
        self.config.local_data_file.mkdir(parents=True, exist_ok=True)

        for csv_dir in self.config.csv_dir:
            Path(csv_dir).mkdir(parents=True, exist_ok=True)

        for i, url in enumerate(self.config.source_URL):
            try:

                file_id = self.extract_file_id(url)
                if file_id:
                    direct_url = f"https://drive.google.com/uc?id={file_id}"
                    output_dir = self.config.csv_dir[i]
                    output = Path(output_dir) / f'{file_id}.csv'
                    logger.info(f"Downloading file from {direct_url} to {output}")
                    gdown.download(direct_url, str(output), quiet=False)
                else:
                    logger.error(f"Failed to extract file ID from URL: {url}")
            except Exception as e:
                logger.error(f"Failed to download {url}: {e}")

    def extract_file_id(self, url: str) -> str:
        """Extract file ID from Google Drive URL."""

        if 'drive.google.com' in url:
            try:
                file_id = url.split('d/')[1].split('/')[0]
                return file_id
            except IndexError:
                return None
        return None