from fastapi import FastAPI
from datetime import datetime
import pickle
# load dateparser and stuff
from CustomUnpickler import CustomUnpickler
from typing import List
from pydantic import BaseModel
import pandas as pd
import numpy as np
import uvicorn
import os

app = FastAPI()
model = CustomUnpickler(open("app/lightgbm.pkl", "rb")).load()

@app.get('/predict/')
async def predict(weather: int, temp: int, felt_temp: int, humidity: int, windspeed: int, date_time: str | None = None):
  if not date_time:
    date_time = datetime.now()

  df = to_df([date_time], [weather], [temp], [felt_temp], [humidity], [windspeed])
  pred = model.predict(df)
  return round(pred[0])

class Features(BaseModel):
  weather: int
  temp: int
  felt_temp: int
  humidity: int
  windspeed: int
  date_time: str | None = None

class FeaturesList(BaseModel):
  data: List[Features]
  count: None = None

@app.post("/predict/")
async def multi_predict(features: FeaturesList):
  current_date = datetime.now()
  for value in features.data:
    if not value.date_time:
      value.date_time = str(current_date)

  features_arrays = [get_array(key, features) for key in ("date_time", "weather", "temp", "felt_temp", "humidity", "windspeed")]
  df = to_df(*features_arrays)

  preds = model.predict(df).round().astype(int)
  features.count = preds.tolist()

  return features

def get_array(key, values):
  return [dict(value)[key] for value in values.data]

def to_df(date_time, weather, temp, felt_temp, humidity, windspeed):
  return pd.DataFrame({
    "datetime": pd.Series(date_time, dtype='str'),
    "weather": pd.Series(weather, dtype='int'),
    "temp": pd.Series(temp, dtype='int'),
    "atemp": pd.Series(felt_temp, dtype='int'),
    "humidity": pd.Series(humidity, dtype='int'),
    "windspeed": pd.Series(windspeed, dtype='int')
  })

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))