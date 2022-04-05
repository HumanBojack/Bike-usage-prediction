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

# Custom API base url
base_api_url = "http://romainbs.azurewebsites.net"

# API METEO => Make changes to not have api key in the code and to transform the response in a 1-4 integer

api_key = "6f6890ed8c566a3b0f5763b583f17182"

lat = "47.751076"

lon ="-120.740135"

url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,current&appid={api_key}&units=metric"

meteo_response = requests.get(url)

# meteo_data = json.loads(meteo_response.text)
meteo_data = meteo_response.json()

cf.set_config_file(offline=True)

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

    url = f"{base_api_url}/predict/?weather={weather}&temp={temp}&felt_temp={atemp}&humidity={humidity}&windspeed={windspeed}"
    if not current_date:
        url += f"&date_time={date_side}"

    pred_response = requests.get(url)
    data = json.loads(pred_response.text)

    st.header(url)
    st.header(data)


# LIVE TIME PREDICTION
features = {"data": []}
for hour in meteo_data["hourly"]:
  features["data"].append(
    {
      "date_time": str(datetime.utcfromtimestamp(hour["dt"])),
      "weather": 1,
      "temp": hour["temp"],
      "felt_temp": hour["feels_like"],
      "humidity": hour["humidity"],
      "windspeed": hour["wind_speed"]
    }
  )

url = f"{base_api_url}/predict"
pred_response = requests.post(url, json=features)
response = pred_response.json() 

df = pd.DataFrame({
    "datetime": [x['date_time'] for x in response['data']],
    "weather": [x['weather'] for x in response['data']],
    "temp": [x['temp'] for x in response['data']],
    "atemp": [x['felt_temp'] for x in response['data']],
    "humidity": [x['humidity'] for x in response['data']],
    "windspeed": [x['windspeed'] for x in response['data']],
    "count": response['count']
  })
    
fig = px.line(df, x="datetime", y="count", title='Croissance de la demande')
st.plotly_chart(fig, use_container_width=True)
st.dataframe(df)

# COLOMNES DE METEO

col1, col2, col3 = st.columns(3)

meteo_atm = df['weather'][0]

temp_atm = df['temp'][0]

# INDICES METEO

meteo_plus_1 = df['weather'][1]

meteo_plus_2 = df['weather'][2]

meteo_plus_3 = df['weather'][3]

# IMAGES A REMPLACER 

image_meteo_1 = "https://openweathermap.org/img/wn/02d@2x.png"
image_meteo_2 = "https://openweathermap.org/img/wn/04d@2x.png"
image_meteo_3 = "https://openweathermap.org/img/wn/09d@2x.png"
image_meteo_4 = "https://openweathermap.org/img/wn/11d@2x.png"

# Premiere colomne

with col1:
  
    st.header("Dans une heure")
    
    if meteo_plus_1 == 1:
      st.write(str(df['temp'][1]), "°C")
      st.image(image_meteo_1)
      
    if meteo_plus_1 == 2:
      st.write(str(df['temp'][1]), "°C")
      st.image(image_meteo_2)
      
    if meteo_plus_1 == 3:
      st.write(str(df['temp'][1]), "°C")
      st.image(image_meteo_3)
      
    if meteo_plus_1 == 4:
      st.write(str(df['temp'][1]), "°C")
      st.image(image_meteo_4)
      
# Deuxieme colomne

with col2:
  
    st.header("Dans deux heures")
    
    if meteo_plus_2 == 1:
      st.write(str(df['temp'][2]), "°C")
      st.image(image_meteo_1)
      
    if meteo_plus_2 == 2:
      st.write(str(df['temp'][2]), "°C")
      st.image(image_meteo_2)
      
    if meteo_plus_2 == 3:
      st.write(str(df['temp'][2]), "°C")
      st.image(image_meteo_3)
      
    if meteo_plus_2 == 4:
      st.write(str(df['temp'][2]), "°C")
      st.image(image_meteo_4)
      
      
# Troisieme colomne

with col3:
  
    st.header("Dans trois heures")
    
    if meteo_plus_3 == 1:
      st.write(str(df['temp'][3]), "°C")
      st.image(image_meteo_1)
      
    if meteo_plus_3 == 2:
      st.write(str(df['temp'][3]), "°C")
      st.image(image_meteo_2)
      
    if meteo_plus_3 == 3:
      st.write(str(df['temp'][3]), "°C")
      st.image(image_meteo_3)
      
    if meteo_plus_3 == 4:
      st.write(str(df['temp'][3]), "°C")
      st.image(image_meteo_4)
    
      
    



    