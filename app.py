from flask import Flask,request,render_template,redirect
import requests
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import psycopg2
from src.mlproject.utils import User
import bcrypt
from src.mlproject.pipelines.prediction_pipelines import CustomData,PredictPipeline
from datetime import datetime

application = Flask(__name__)

app = application

API_KEY = '71d2db972c917a224b14a17b03202088'



@app.route('/home')

def index():
    return render_template('home.html')

@app.route('/signup' , methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name= request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name,email,password)
        new_user.authentication_postgres_data()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        
        if User.check_password(email,password):
            return redirect('/intro')
        else:
            return render_template('login.html',error = 'Invalid user')

    return render_template('login.html')


@app.route("/forgot_password",methods = ['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if User.forgot_password(email,password):
            return redirect('/login')
        
    return render_template('forgot.html')

@app.route("/intro",methods=['GET','POST'])
def intro():
    return render_template('intro.html')

@app.route("/dashboard",methods = ['GET','POST'])
def dashboard():
    if request.method == 'GET':
         return render_template('dashboard.html')
    
    else:
        data= CustomData(
            month = request.form.get('month'),
            precipitation = request.form.get('precipitation'),
            temp_max=request.form.get('maxTemp'),
            temp_min=request.form.get('minTemp'),
            wind = request.form.get('windSpeed')
        )

        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        result = predict_pipeline.predict(pred_df)
        weather_conditions = {0: "Drizzle", 1: "Fog", 2: "Rain", 3: "Snow", 4: "Sun"}
        weather_result = weather_conditions.get(result[0], "Unknown")
        return render_template('dashboard.html',result=weather_result)
    

@app.route("/predict",methods = ['GET','POST'])
def fetch_weather():
    CITY = request.form.get('city')
    BASE_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'
    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract required data
        main = data['main']
        wind = data['wind']
        weather = data['weather'][0]
        
        
        prec = data.get('rain', {}).get('1h', 0)  # Rain in the last 1 hour (if available)
        
        print(f"Weather in {CITY}:")
        print(f"Temperature Max: {main['temp_max']}°C")
        print(f"Temperature Min: {main['temp_min']}°C")
        print(f"Wind Speed: {wind['speed']} m/s")
        print(f"Precipitation (last 1h): {prec} mm")
        real_data_input_dict = { 
            "month":[datetime.now().month],
            "precipitation":[prec],
            "temp_max": [main['temp_max']],
            "temp_min":[main['temp_min']],
            "wind" : [wind['speed']]
        }
          
        df = pd.DataFrame(real_data_input_dict)  
        predict_pipe = PredictPipeline()
        result = predict_pipe.predict(df)
        weather_conditions = {0: "Drizzle", 1: "Fog", 2: "Rain", 3: "Snow", 4: "Sun"}
        weather_result = weather_conditions.get(result[0], "Unknown")
        return render_template('auto.html',result=weather_result)

    else:
        print(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
    

@app.route('/mode', methods = ['GET','POST'])
def mode():
    return render_template('mode.html')




if __name__ =="__main__":
    app.run(debug = True)