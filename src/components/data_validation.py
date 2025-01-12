import os
import pandas as pd
from src import logger
from src.entity.config_entity import (DataValidationConfig)


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            validation_status = True
            csv_files = [f for f in os.listdir(self.config.csv_dir) if f.endswith('.csv')]

            if not csv_files:
                raise ValueError("No CSV files found in the provided directory")

            for csv_file in csv_files:
                csv_path = os.path.join(self.config.csv_dir, csv_file)

                data = pd.read_csv(csv_path)
                all_cols = list(data.columns)

                all_schema = self.config.all_schema.keys()

                for col in all_cols:
                    if col not in all_schema:
                        validation_status = False
                        print(f"Column '{col}' in file '{csv_file}' is not in the schema.")

            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            print(f"Error occurred: {e}")
            raise e