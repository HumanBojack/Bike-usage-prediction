from fastapi import FastAPI
from datetime import datetime
import pickle
# load dateparser and stuff
from CustomUnpickler import CustomUnpickler
import pandas as pd
import uvicorn
import os

app = FastAPI()
model = CustomUnpickler(open("app/lightgbm.pkl", "rb")).load()

@app.get('/predict/')
async def predict(weather: int, temp: int, felt_temp: int, humidity: int, windspeed: int, date_time: str | None = None):
  if not date_time:
    date_time = datetime.now()
    
  df = pd.DataFrame({
    "datetime": pd.Series([date_time], dtype='str'),
    "weather": pd.Series([weather], dtype='int'),
    "temp": pd.Series([temp], dtype='int'),
    "atemp": pd.Series([felt_temp], dtype='int'),
    "humidity": pd.Series([humidity], dtype='int'),
    "windspeed": pd.Series([windspeed], dtype='int')
  })

  pred = model.predict(df)
  return round(pred[0])

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))