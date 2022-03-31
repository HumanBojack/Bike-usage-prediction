import pandas as pd
import cufflinks as cf 
import streamlit as st
from sklearn.base import BaseEstimator,TransformerMixin
import pickle 
import requests
from datetime import datetime
import json
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

# API METEO => Make changes to not have api key in the code and to transform the response in a 1-4 integer
# 

api_key = "6f6890ed8c566a3b0f5763b583f17182"

lat = "47.751076"

lon ="-120.740135"

url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,current&appid={api_key}&units=metrics"

response = requests.get(url)

meteo_data = json.loads(response.text)

cf.set_config_file(offline=True)


# CUSTOM DATAPARSER POUR FAIRE FONCTIONNER LE MODELE
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
    
# CHARGEMENT DU MODELE DE PREDICTION

model = pickle.load(open("lightgbm.pkl", "rb"))


# Sidebar

# CUSTOM DATE PREDICTION
current_date = st.sidebar.checkbox("Date actuelle", value=True)

if not current_date:

    d = st.sidebar.date_input(
        "Jour",
        datetime.now())
    time = st.sidebar.time_input('Prédire cette heure', datetime.now())
    date_side = datetime.combine(d, time)

weather = st.sidebar.number_input('Insert weather', step=1)

temp = st.sidebar.number_input('Insert temp', step=1)

atemp = st.sidebar.number_input('Insert atemp', step=1)

humidity = st.sidebar.number_input('Insert humidity', step=1)

windspeed = st.sidebar.number_input('Insert windspeed', step=1)

validation = st.sidebar.button('Validez votre choix')

if validation : 

    url = f"http://romainbs.azurewebsites.net/predict/?weather={weather}&temp={temp}&felt_temp={atemp}&humidity={humidity}&windspeed={windspeed}"
    if not current_date:
        url += f"&date_time={date_side}"

    response = requests.get(url)
    data = json.loads(response.text)

    st.header(url)
    st.header(data)


# LIVE TIME PREDICTION
for i in range(0,47):
    
    j = meteo_data["hourly"][i]
        
    lst = []
    
    
    # lst.append(datetime.fromtimestamp(t))
    lst.append(j["dt"])
    
    #weather
    lst.append(0)
    #temp
    lst.append(j["temp"])
    #atemp
    lst.append(j["feels_like"])
    #humidity
    lst.append(j["humidity"])
    #windspeed
    lst.append(j["wind_speed"])
    
    df = df.append(pd.Series(lst, index =['datetime', 'season', 'holiday', 'workingday', 'weather', 'temp',
    'atemp', 'humidity', 'windspeed'] ), ignore_index=True)
    
transform_data = model["preprocessor"].transform(df)
    
pred = model['model'].predict(transform_data)
    
df['label'] = pred
fig = px.line(df, x="datetime", y="label", title='Croissance de la demande')
st.plotly_chart(fig, use_container_width=True)
st.dataframe(df)




    