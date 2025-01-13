import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
import joblib
import os
from src import logger
from src.entity.config_entity import (DataTransformationConfig)

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
    
    def remove_highly_correlated_features(self, df, threshold=0.95):
        corr_matrix = df.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
        return df.drop(columns=to_drop)
    
    def train_test_spliting(self):
        data = pd.read_csv(self.config.data_path)
        X = data.drop(['account_number', 'bad_flag'], axis=1)
        y = data['bad_flag']
        missing_pct = (X.isnull().sum() / len(X)) * 100
        cols_to_drop = missing_pct[missing_pct > 70].index
        X_cleaned = X.drop(columns=cols_to_drop)
        numeric_cols = X_cleaned.select_dtypes(include=['float64', 'int64']).columns
        X_cleaned[numeric_cols] = X_cleaned[numeric_cols].fillna(X_cleaned[numeric_cols].median())
        X_cleaned = self.remove_highly_correlated_features(X_cleaned, threshold=0.95)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_cleaned)
        X_scaled = pd.DataFrame(X_scaled, columns=X_cleaned.columns)
        final_df = pd.concat([X_scaled, y], axis=1)
        train, test = train_test_split(final_df, test_size=0.25, random_state=42, stratify=y)
        
        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)

        joblib.dump(scaler, os.path.join(self.config.root_dir, "scaler.joblib"))
        
        logger.info("Completed data transformation")
        logger.info(f"Training set shape: {train.shape}")
        logger.info(f"Test set shape: {test.shape}")
        
        return train, test