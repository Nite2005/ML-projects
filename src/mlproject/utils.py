import os 
import sys
from src.mlproject.exception import CustomException 
from src.mlproject.logger import logging
import pandas as pd
from dotenv import load_dotenv
import psycopg2
import pickle 
import dill 
import numpy as np
from sklearn.model_selection import GridSearchCV
import bcrypt
from dataclasses import  dataclass



load_dotenv()

host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("dbname")
port = os.getenv("port")

def read_postgres_data():
    logging.info("Reading Postgresql database started")
    try:
    
        logging.info("start to Establish a connection to the database")

        mydb = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            dbname = db,
            port = port
        )
        logging.info("connection established successfully")
        
        #create a cursor object to interact with the database
        cursor = mydb.cursor()

        #Execute query
        query = 'select * from weather_data'
        cursor.execute(query)

        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
        cursor.close()
        mydb.close()
        return df

    except Exception as e:
        logging.info("Connection establish not successful")
        raise CustomException(e,sys)
    
def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
    
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
        
    except Exception as e:
        raise CustomException(e,sys)

class User:
    def __init__(self, name, email, passwrd):
        self.name = name
        self.email = email
        self.passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def authentication_postgres_data(self):
        """Stores user details in the PostgreSQL database."""
        logging.info("Connecting to PostgreSQL database to insert user data.")
        try:
            # Establish database connection
            conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                dbname=db,
                port=port
            )
            cursor = conn.cursor()
            cursor.execute("SELECT name, email FROM weather_users WHERE email = %s", (self.email,))
            user_data = cursor.fetchone()

            if user_data is None:
                
            # Insert user into database
                query = "INSERT INTO weather_users (name, email, password) VALUES (%s, %s, %s);"
                cursor.execute(query, (self.name, self.email, self.passwrd))

            conn.commit()
            cursor.close()
            conn.close()

            logging.info("User registered successfully in the database.")

        except Exception as e:
            logging.error("Failed to insert user data.")
            raise CustomException(e, sys)

    @staticmethod
    def check_password(email, passwrd):
        """Checks if the provided password matches the stored hashed password."""
        try:
            conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                dbname=db,
                port=port
            )
            cursor = conn.cursor()

            cursor.execute("SELECT name, email, password FROM weather_users WHERE email = %s", (email,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()

            if user_data:
                stored_password = user_data[2]
                if bcrypt.checkpw(passwrd.encode('utf-8'), stored_password.encode('utf-8')):
                    return True
                else:
                    return False
            else:
                return False  # User not found

        except Exception as e:
            logging.error("Error while verifying user password.")
            raise CustomException(e, sys)
    

    def forgot_password(email,new_password):
        try:
            logging.info("Establishing a connection for forgot password")
            conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                dbname=db,
                port=port
            )
            cursor = conn.cursor()
            new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            # Check if the user exists
            cursor.execute("SELECT name, email FROM weather_users WHERE email = %s", (email,))
            user_data = cursor.fetchone()

            if user_data is None:
                raise CustomException(f"No user found with email {email}", sys)

            # Update the password
            cursor.execute("UPDATE weather_users SET password = %s WHERE email = %s", (new_password, email))
            conn.commit()  # Save the changes

            logging.info("Password updated successfully")

            cursor.close()
            conn.close()
            return True

        except Exception as e:
            raise CustomException(e, sys)

        
        
    





        