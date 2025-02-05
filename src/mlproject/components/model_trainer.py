import os
import sys
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from sklearn.linear_model import LogisticRegression
from dataclasses import dataclass
from src.mlproject.utils import save_object
from sklearn.metrics import accuracy_score


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts",'model.pkl')


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()


    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split training and test input data")
            x_train,y_train,x_test,y_test =(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]

            )
            

            lr = LogisticRegression(C=10, max_iter=300, penalty=None, solver='saga')
            lr.fit(x_train,y_train)
            pred = lr.predict(x_test)
            print(accuracy_score(y_test,pred))
            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = lr
            )
             

            logging.info("Model training completed and saved successfully")
            return lr

        except Exception as e:
            raise CustomException(e,sys)


