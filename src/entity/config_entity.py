from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_URL: List[str]
    local_data_file: Path
    csv_dir: List[Path]