import numpy, pandas, requests, json
from datetime import datetime
import matplotlib.pyplot as plot
 
class ExponentialMovingAverage:
    def __init__(self, times, closings):
        self.df = pandas.DataFrame({'Close':closings}, index=times)
    def add_data(self, times, closings):
        new_df = pandas.DataFrame({'Date':times, 'Close':closings})
        self.df = self.df.append(new_df, ignore_index=True)
    def ema(self, periods):
        ema_df = self.df.ewm(span=periods).mean()
        return ema_df
 

