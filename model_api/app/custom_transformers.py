from sklearn.base import BaseEstimator,TransformerMixin
import pandas as pd

HOLIDAYS = ["01-01", "19-06", "04-07", "11-11", "25-12"] # This only uses the fixed holidays

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
                "season": X.dt.month % 12 // 3 + 1,
                # "holiday":  X.dt.strftime('%d-%m').isin(HOLIDAYS),
                "workingday": (X.dt.weekday.isin(range(5))) & (X.dt.strftime('%d-%m').isin(HOLIDAYS) == False),
            }
        )
        return return_X