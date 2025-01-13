from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_URL: List[str]
    local_data_file: Path
    csv_dir: List[Path]

@dataclass
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    csv_dir: Path
    all_schema: dict

@dataclass
class DataTransformationConfig:
    root_dir:Path
    data_path: Path