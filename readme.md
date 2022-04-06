# Bike Usage Prediction

# What is it?
This repository contains a few things, mainly :
- a **machine learning model**, trained to predict the number of bikes that would be taken in Washington DC given some conditions.
- an **app** (streamlit) who serves as a graphical interface for the model, it also fetches the weather forecast in order to save you some time
- an **api** (fastapi), used to make the model and the app **communicate**

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
