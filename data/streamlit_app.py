import pandas as pd
import cufflinks as cf 
import streamlit as st
from sklearn.base import BaseEstimator,TransformerMixin
import pickle 
import requests
from datetime import datetime
import json

api_key = "6f6890ed8c566a3b0f5763b583f17182"

lat = "47.751076"

lon ="-120.740135"

url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,current&appid={api_key}&units=metrics"
response = requests.get(url)
meteo_data = json.loads(response.text)

cf.set_config_file(offline=True)
pd.set_option('display.max_columns',25)


class DateParser(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = pd.to_datetime(X["datetime"])
        return_X = pd.DataFrame(
            {
                "weekday": X.dt.weekday,
                "hour": X.dt.hour,
                "month": X.dt.month,
                "year": X.dt.year,
            }
        )
        return return_X
    
model = pickle.load(open("lightgbm.pkl", "rb"))


# Sidebar

season = st.sidebar.number_input('Insert season')

holiday = st.sidebar.number_input('Insert holiday')

workingday = st.sidebar.number_input('Insert workingday')

weather = st.sidebar.number_input('Insert weather')

temp = st.sidebar.number_input('Insert temp')

atemp = st.sidebar.number_input('Insert atemp')

humidity = st.sidebar.number_input('Insert humidity')

windspeed = st.sidebar.number_input('Insert windspeed')

validation = st.sidebar.button('Validez votre choix')


df = pd.DataFrame(columns=['datetime', 'season', 'holiday', 'workingday', 'weather', 'temp',
       'atemp', 'humidity', 'windspeed'])

    
for i in range(0,47):
    
    j = meteo_data["hourly"][i]
        
    lst = []
    
    t = float(j["dt"])
    # lst.append(datetime.fromtimestamp(t))
    lst.append('2011-04-16 03:00:00')
    lst.append(0)
    lst.append(0)
    lst.append(0)
    lst.append(0)
    lst.append(j["temp"])
    lst.append(j["feels_like"])
    lst.append(j["humidity"])
    lst.append(j["wind_speed"])
    
    df = df.append(pd.Series(lst, index =['datetime', 'season', 'holiday', 'workingday', 'weather', 'temp',
    'atemp', 'humidity', 'windspeed'] ), ignore_index=True)
    
transform_data = model["preprocessor"].transform(df)
    
pred = model['model'].predict(transform_data)
    
st.dataframe(pred)

if validation : 
    
    # Creation du dataset
 
    df_side = pd.DataFrame(columns=['datetime', 'season', 'holiday', 'workingday', 'weather', 'temp',
       'atemp', 'humidity', 'windspeed'])    
    
    
    
    # Prediction data
    
    transform_data = model["preprocessor"].transform(df_side)
    
    pred_side = model['model'].predict(transform_data)
    
    st.dataframe(pred_side)
    


    