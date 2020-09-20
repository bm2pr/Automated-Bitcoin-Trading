from robin_stocks import authentication, robin_stocks, crypto, orders
import matplotlib.pyplot as plot
import dateutil.parser
import Config
import time
import json, pandas, numpy
from datetime import datetime, timedelta


authentication.login(Config.USERNAME, Config.PASSWORD)

'''
def short_long_ema():
    ema_x = ExponentialMovingAverage(times[:120], closings[:120])
    
    usd_val = 10
    btc_val = 0
    bought = False
    for x in range(120, len(closings)):
        if bought:
            btc_val = btc_val + ((closings[x] - closings[x-1]) / closings[x-1]) * btc_val
        ema_x = ExponentialMovingAverage(times[:x+1], closings[:x+1])
        ema_average = ema_x.ema(200)
        plot.plot(ema_x.df, color='blue', label='Orig')
        plot.plot(ema_average, color='red', label='EMA')
        plot.legend()
        plot.show()
        print(times[x])
        print(closings[x])
        if closings[x] > ema_average.values[x] and bought:
            usd_val = btc_val
            btc_val = 0
            bought = False
        elif closings[x] < ema_average.values[x] and closings[x-1] < ema_average.values[x-1] and not bought:
            btc_val = usd_val
            usd_val = 0
            bought = True
        if bought:
            print('Holding bitcoin {btc}'.format(btc=btc_val))
        else:
            print('Holding usd {usd}'.format(usd=usd_val))
    print('{usd}:{btc}'.format(usd=usd_val, btc=btc_val))
'''
def predicted_values(times, closings, x):
 
    curr_time = times[x-30]
 
    y1 = closings[x-70]
    y2 = closings[x-30]
 
    change_per_15_second = (y2-y1)/40
    
    prediction_df = pandas.DataFrame({'Price':[y2]}, index=[curr_time])
    
    for x in range(1, 31):
        curr_time = curr_time + timedelta(seconds=15)
        prediction_df = prediction_df.append(pandas.DataFrame({'Price':[y2 + x*change_per_15_second]}, index=[curr_time]))
    
    return prediction_df
 



def run():
 
    #loop_counter = 0
    worth = 0
    bought = False
    curr_time, curr_price = get_data()

    for x in range(70, 240):
        # Test prediction against current price
        difference = curr_price[x] - curr_price[x - 1]
        if bought:
            worth = worth + difference

        # Make new prediction with current price
        pred_values = predicted_values(curr_time, curr_price, x)
        plot.plot(pred_values)
        plot.plot(curr_time, curr_price)
        plot.show()
        print(pred_values)
        print(curr_time[x])
        pred_value_at_time = pred_values.loc[curr_time[x]]['Price']
        term_increasing = pred_values['Price'].values[0] < pred_values['Price'].values[1]
        if curr_price[x] > pred_value_at_time and term_increasing:
            bought = True
            #buy

        elif pred_value_at_time < curr_price[x] and not term_increasing:
            bought = False
            #sell
    print(worth)
        
def get_data():
    ret_val = crypto.get_crypto_historical('BTC', '15second', 'hour', '24_7')
    data = ret_val['data_points']
    output_file = open('Robin Stocks.txt', 'w')
    output_file.write(json.dumps(data, indent=2))
    times = []
    closings = []
    for x in data:
        times.append(dateutil.parser.parse(x['begins_at']))
        closings.append(float(x['close_price']))
 
    return times, closings
 
run()