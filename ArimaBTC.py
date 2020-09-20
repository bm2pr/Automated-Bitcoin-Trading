import pandas as ps
import numpy as np 
import requests as req
import json, time, collections
from datetime import datetime
import matplotlib.pyplot as plot
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller

class ArimaBTC():
    p, d, q = 3, 1, 0
    def __init__(self, train_data_times, train_data_closings):
        self.df = ps.DataFrame({'Date':train_data_times, 'Close':train_data_closings})
        self.df.dropna()
        print(self.df)
        #self.test_stationarity(self.df['Close'])
        self.arima_model = ARIMA(self.df['Close'], order=(self.p,self.d,self.q))
        self.arima_results = self.arima_model.fit(disp=-1)
    def forecast(self, num_steps):
        result = self.arima_results.forecast(num_steps)
        #pred_time = self.df['Date'].tail(1).iat[0] + 1
        return result[0][:num_steps]
    def add_train_data(self, train_data_times, train_data_closings):
        new_df = ps.DataFrame({'Date':train_data_times, 'Close':train_data_closings})
        self.df = self.df.append(new_df, ignore_index=True)
        self.arima_model = ARIMA(self.df['Close'], order=(self.p,self.d,self.q))
        self.arima_results = self.arima_model.fit(disp=-1)
    def test_stationarity(self, x):
        #Determing rolling statistics
        rolmean = x.rolling(window=10,center=False).mean()

        rolstd = x.rolling(window=5,center=False).std()
        
        #Plot rolling statistics:
        plot.plot(x, color='blue',label='Original')
        plot.plot(rolmean, color='red', label='Rolling Mean')
        plot.plot(rolstd, color='black', label = 'Rolling Std')
        plot.legend(loc='best')
        plot.title('Rolling Mean & Standard Deviation')
        plot.show()
        
        #Perform Dickey Fuller test    
        result=adfuller(x)
        print('ADF Stastistic: %f'%result[0])
        print('p-value: %f'%result[1])
        for key,value in result[4].items():
            if result[0]>value:
                print("The graph is non stationery")
                break
            else:
                print("The graph is stationery")
                break
        print('Critical values:')
        for key,value in result[4].items():
            print('\t%s: %.3f ' % (key, value))



api_url = 'https://api.pro.coinbase.com/'
output_file = open("TestData.txt", "w")
res_json = req.get(api_url + 'products/BTC-USD/candles').json()
output_file.write(json.dumps(res_json, indent=2))
times = []
closings = []
for x in res_json:
    #tm = time.gmtime(x[0])
    #times.append('{hour}:{min}'.format(hour=tm.tm_hour, min=tm.tm_min, sec=tm.tm_sec))
    times.append(datetime.fromtimestamp(x[0]))
    closings.append(x[4])
closings.reverse()
times.reverse()
'''
new_closings = []
for i in range(len(closings) - 1):
    new_closings.append(closings[i+1] - closings[i])

closings = new_closings
del closings[0]
del times[0]
'''
log_closings = np.log(closings)
num_trainings = 250
num_predictions = 20

test_arima = ArimaBTC(times[:num_trainings], log_closings[:num_trainings])

plot.plot(times[:num_trainings + num_predictions], closings[:num_trainings + num_predictions], color='blue')
num_mismatches = 0
predictions = []
for i in range(num_predictions):
    predictions.append(np.exp(test_arima.forecast(1)))
    test_arima.add_train_data([times[i + num_trainings]], [log_closings[i + num_trainings]])
    predicted_delta = predictions[-1] - closings[i + num_trainings - 1]
    actual_delta = closings[i + num_trainings] - closings[i + num_trainings - 1]
    if (predicted_delta < 0 and actual_delta > 0) or (predicted_delta > 0 and actual_delta < 0):
        num_mismatches = num_mismatches + 1
print('Percent Incorrect = {val}'.format(val=num_mismatches/num_predictions))
plot.plot(times[num_trainings:num_trainings + num_predictions], predictions, color='red')
plot.show()
