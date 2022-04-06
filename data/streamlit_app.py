import pandas as pd
import cufflinks as cf
import streamlit as st
import requests
from datetime import datetime
import json
import plotly.express as px
import re
from dotenv import load_dotenv
import os

load_dotenv()

# Custom API base url
base_api_url = os.environ.get("PREDICTION_API_URL")

api_key = os.environ.get("WEATHER_API")

lat = "38.907367783128684"

lon = "-77.03659139978163"

url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,current&appid={api_key}&units=metric"

meteo_data = requests.get(url).json()

cf.set_config_file(offline=True)

# Sidebar

# CUSTOM DATE PREDICTION
current_date = st.sidebar.checkbox("Date actuelle", value=True)

if not current_date:

    d = st.sidebar.date_input("Jour", datetime.now())
    time = st.sidebar.time_input("Prédire cette heure", datetime.now())
    date_side = datetime.combine(d, time)

weather = st.sidebar.number_input("Indice météo", 1, 4, step=1)

temp = st.sidebar.number_input("Température", -40, 50, 0, 1)

atemp = st.sidebar.number_input("Température ressentie", -40, 50, 0, 1)

humidity = st.sidebar.number_input("Humidité (%)", 0, 100, step=1)

windspeed = st.sidebar.number_input("Vitesse du vent (km/h)", 0, 100, step=1)

validation = st.sidebar.button("Validez votre choix")

if validation:

    url = f"{base_api_url}/predict/?weather={weather}&temp={temp}&felt_temp={atemp}&humidity={humidity}&windspeed={windspeed}"
    if not current_date:
        url += f"&date_time={date_side}"

    data = requests.get(url).json()

    st.header(data)

# Calculate the weather level (1 to 4) based on conditions
def get_weather_level(hour):
    weather_level = []
    for weather in hour["weather"]:
        weather_id = int(weather["id"])

        if weather_id == 301 | 300 <= weather_id <= 301:
            weather_level.append(2)
        elif (
            702 <= weather_id <= 761 |
            600 <= weather_id <= 601 |
            200 <= weather_id <= 201 ):
            weather_level.append(3)
        elif (
            502 <= weather_id <= 531 |
            302 <= weather_id <= 321 |
            202 <= weather_id <= 232 |
            602 <= weather_id <= 622 |
            762 <= weather_id <= 781 ):
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
            "windspeed": hour["wind_speed"],
        }
    )

url = f"{base_api_url}/predict"
pred_response = requests.post(url, json=features)
response = pred_response.json()

df = pd.DataFrame(
    {
        "datetime": [x["date_time"] for x in response["data"]],
        "weather": [x["weather"] for x in response["data"]],
        "temp": [x["temp"] for x in response["data"]],
        "atemp": [x["felt_temp"] for x in response["data"]],
        "humidity": [x["humidity"] for x in response["data"]],
        "windspeed": [x["windspeed"] for x in response["data"]],
        "count": response["count"],
    }
)

fig = px.line(df, x="datetime", y="count", title="Croissance de la demande")
st.plotly_chart(fig, use_container_width=True)
st.dataframe(df)

# Three hours weather prediction
def meteo_url(icon):
    return f"https://openweathermap.org/img/wn/{icon}@2x.png"


for index, col in enumerate(st.columns(3)):
    with col:

        hour = re.search("((?<= 0)[0-9]|(?<= )[1-9][0-9])", df["datetime"][index + 1])
        st.header(f"À {hour.group()}h")

        st.write(str(df["temp"][index + 1]), "°C")
        icon = meteo_data["hourly"][index + 1]["weather"][0]["icon"]
        st.image(meteo_url(icon))
