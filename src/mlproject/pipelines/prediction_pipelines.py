import sys
import pandas as pd
from src.mlproject.exception import CustomException
from src.mlproject.utils import load_object




class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path = 'artifacts\model.pkl'
            preprocessor_path = 'artifacts\preprocessor.pkl'
            model = load_object(file_path=model_path)
            preprocesor =  load_object(file_path = preprocessor_path)
            data_scaled = preprocesor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)


class CustomData:
    def __init__(self,
                 month:int,
                 precipitation:float,
                 temp_max:float,
                 temp_min:float,
                 wind:float):
        self.month = month
        self.precipitation = precipitation
        self.temp_max = temp_max
        self.temp_min = temp_min
        self.wind=wind
    

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "month":[self.month],
                "precipitation":[self.precipitation],
                "temp_max":[self.temp_max],
                "temp_min":[self.temp_min],
                "wind":[self.wind]
            }

            return pd.DataFrame(custom_data_input_dict)
        

        except Exception as e:
            raise CustomException(e,sys)
    