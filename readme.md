# Bike Usage Prediction

# What is it?
This repository contains a few things, mainly :
- a **[machine learning model](#the-model)**, trained to predict the number of bikes that would be taken in Washington DC given some conditions.
- an **[app](#the-application)** (streamlit) who serves as a graphical interface for the model, it also fetches the weather forecast in order to save you some time
- an **[api](#the-api)** (fastapi), used to make the model and the app **communicate**

# The model
The model we are using is [LightGBM](https://lightgbm.readthedocs.io/en/latest/).
>LightGBM is a gradient boosting framework that uses tree based learning algorithms. It is designed to be distributed and efficient with the following advantages:
> - Faster training speed and higher efficiency.
> - Lower memory usage.
> - Better accuracy.
> - Support of parallel, distributed, and GPU learning.
> - Capable of handling large-scale data.

We also tried other models that we ended up not using, such as:
- catboost
- random forest

## Features
The model needs **6** parameters in order to make a prediction:
- A weather indice [int between 1 and 4], describing how the weather is, [more informations](https://www.kaggle.com/competitions/bike-sharing-demand/data).
- The temperature [int] in Celsius
- The felt temperature [int] in Celsius
- The humidity percentage [int]
- The windspeed [int] in KMH
- The date and time [str] ex: '2022-04-05 12:34:25.302959'

# The application
The application was made using **streamlit** in order to have a simple but good result while **saving development time**.

The **goal** of this application is **to provide easier predictions** to the user. This is done with an **easy to understand interface** giving you predictions for the next 48 hours as you enter the website. You can also make a **custom predictions** with the left bar.

# The API
The API was made using [FastAPI](https://fastapi.tiangolo.com/), which made it's development quite fast.

Then, it was made into a docker container and deployed on azure.
You can find it [here](romainbs.azurewebsites.net/docs) at the time of writing.

Two useful methods exist:

## **[GET]** /predict/
This method is used in order to **easily** make a single prediction.

In order to make a prediction, you need to specify the parameters:
- weather [int]
- temp [int]
- felt_temp [int]
- humidity [int]
- windspeed [int]
- date_time [str] optional

For more information, see [features](#features).

In return, you will get **an integer** representing the number of bikes that should be taken for this set of parameters.

## **[POST]** /predict/
This method is used in order to do **multiple** predictions.

The body of the request needs to be in the form of (here for a single prediction):
```json
{
  "data": [
    {
      "weather": "int",
      "temp": "int",
      "felt_temp": "int",
      "humidity": "int",
      "windspeed": "int",
      "date_time": "str / optional"
    }
  ]
}
```
For more information, see [features](#features).