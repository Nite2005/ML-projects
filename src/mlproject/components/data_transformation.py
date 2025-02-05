import sys
import os
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from src.mlproject.utils import save_object
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numeric_feature = ['month', 'precipitation', 'temp_max', 'temp_min', 'wind']
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scalar', StandardScaler())
            ])

            preprocessor = ColumnTransformer(
                transformers=[  # Corrected part
                    ('num_pipeline', num_pipeline, numeric_feature)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Successfully read data.")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "weather_encoded"
            numerical_features = ['month', 'precipitation', 'temp_max', 'temp_min', 'wind']

            # Splitting train and test data
            train_x = train_df.drop(columns=[target_column_name], axis=1)
            train_y = train_df[target_column_name]

            test_x = test_df.drop(columns=[target_column_name], axis=1)
            test_y = test_df[target_column_name]

            logging.info("Applying preprocessing transformations.")

            train_array = preprocessing_obj.fit_transform(train_df)
            test_array = preprocessing_obj.transform(test_df)

            train_arr = np.c_[
                train_array,np.array(train_y)
            ]
            test_arr = np.c_[
                test_array,np.array(test_y)
            ]

            

            logging.info(f"Saving preprocessing object to {self.data_transformation_config.preprocessor_obj_file_path}")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return ( 
            train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
