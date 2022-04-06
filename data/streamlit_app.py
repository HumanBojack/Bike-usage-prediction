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
import re

# Custom API base url
base_api_url = "http://romainbs.azurewebsites.net"

# API METEO => Make changes to not have api key in the code and to transform the response in a 1-4 integer

api_key = "6f6890ed8c566a3b0f5763b583f17182"

lat = "38.907367783128684"

lon ="-77.03659139978163"

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

# Calculate the weather level (1 to 4) based on conditions
def get_weather_level(hour):
  weather_level = []
  for weather in hour["weather"]:
    weather_id = int(weather["id"])

    if weather_id == 301 | 300<=weather_id<=301:
      weather_level.append(2)
    elif 702<=weather_id<=761 | 600<=weather_id<=601 | 200<=weather_id<=201:
      weather_level.append(3)
    elif 502<=weather_id<=531 | 302<=weather_id<=321 | 202<=weather_id<=232 | 602<=weather_id<=622 | 762<=weather_id<=781:
      weather_level.append(4)
    else:
      weather_level.append(1)

  return max(weather_level)

# LIVE TIME PREDICTION
features = {"data": []}
for hour in meteo_data["hourly"]:
  features["data"].append(
    {
      "date_time": str(datetime.utcfromtimestamp(hour["dt"])),
      "weather": get_weather_level(hour),
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

# Three hours weather prediction
def meteo_url(icon):
  return f"https://openweathermap.org/img/wn/{icon}@2x.png"

for index, col in enumerate(st.columns(3)):
  with col:
    
      hour = re.search("((?<= 0)[0-9]|(?<= )[1-9][0-9])", df['datetime'][index + 1])
      st.header(f"À {hour.group()}h") 

      st.write(str(df['temp'][index + 1]), "°C")
      icon = meteo_data["hourly"][index + 1]["weather"][0]["icon"]
      st.image(meteo_url(icon))
    



    