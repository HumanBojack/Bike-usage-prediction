import pandas as pd
import cufflinks as cf 
import streamlit as st
from sklearn.base import BaseEstimator,TransformerMixin
import pickle 
import requests
import datetime
import json
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

# API METEO

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
d = st.sidebar.date_input(
     "Jour",
     datetime.date(2022, 3, 28))

time = st.sidebar.time_input('Prédire cette heure', datetime.time(8, 45))

season = st.sidebar.number_input('Insert season')

holiday = st.sidebar.number_input('Insert holiday')

workingday = st.sidebar.number_input('Insert workingday')

weather = st.sidebar.number_input('Insert weather')

temp = st.sidebar.number_input('Insert temp')

atemp = st.sidebar.number_input('Insert atemp')

humidity = st.sidebar.number_input('Insert humidity')

windspeed = st.sidebar.number_input('Insert windspeed')

validation = st.sidebar.button('Validez votre choix')

date_side = datetime.datetime.combine(d, time)

df = pd.DataFrame(columns=['datetime', 'season', 'holiday', 'workingday', 'weather', 'temp',
       'atemp', 'humidity', 'windspeed'])

if validation : 
    
    # Creation du dataset
    df_side = []
    lst_side = [] 
    
    lst_side = [date_side, season,holiday,workingday,weather,temp,atemp,humidity, windspeed]
    
    df_side = df_side.append(pd.Series(lst_side, index =['datetime', 'season', 'holiday', 'workingday', 'weather', 'temp',
    'atemp', 'humidity', 'windspeed'] ), ignore_index=True)
    # Prediction data
    
    transform_data_side = model["preprocessor"].transform(df_side)
    
    pred_side = model['model'].predict(transform_data_side)
    
    st.dataframe(pred_side)
    


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




    