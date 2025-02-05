from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
from src.mlproject.components.data_ingestion import DataIngestion
from src.mlproject.components.data_ingestion import DataIngestionConfig
from src.mlproject.components.data_transformation import DataTransformation
from src.mlproject.components.data_transformation import DataTransformationConfig
from src.mlproject.components.model_trainer import ModelTrainerConfig
from src.mlproject.components.model_trainer import ModelTrainer
import os
import sys







if __name__ == "__main__":
    logging.info("The execution has starte")

    try:
        #data_ingestion_config = DataingestionConfig()
        data_ingestion = DataIngestion()
        train_data_path,test_data_path = data_ingestion.initiate_data_ingestion()

        #data_transformation_config = DataTransformationConfig()
        data_transformation = DataTransformation()
        train_array,test_array,_ = data_transformation.initiate_data_transformation(train_data_path,test_data_path)


        model_trainer = ModelTrainer()
        model_trainer.initiate_model_trainer(train_array,test_array)


    except Exception as e:
        raise CustomException(e,sys)
        #pass
