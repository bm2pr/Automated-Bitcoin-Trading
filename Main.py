import numpy, pandas, requests, json, Config
from robin_stocks import authentication, crypto
from datetime import datetime
from Driver import Driver
import matplotlib.pyplot as plot
from EMA import ExponentialMovingAverage
import time, dateutil.parser
 
 
 
def find_times():
    ret_val = crypto.get_crypto_historical('BTC', '15second', 'hour', '24_7')
    data = ret_val['data_points']
    times = []
    closings = []
    for x in data:
        times.append(dateutil.parser.parse(x['begins_at']))
        closings.append(float(x['close_price']))
 
    return times, closings
 
 
# Set up chrome web driver
authentication.login(Config.USERNAME, Config.PASSWORD)
driver = Driver()
driver.login_method()
'''
while True:
    
    # Calculate exponential moving averages
 
    times, closings = find_times()
    time_now = datetime.now()
    if time_now.second < 15:
        bought = driver.bought()
        ema = ExponentialMovingAverage(times, closings)
        ema_ref = ema.ema(200)
        if bought:
            sell_price = driver.get_curr_sell_price()
            if sell_price > ema_ref.values[-1]:
                driver.sell()
                print('Sold at time {time} with sell price {price} and closings {cl}'.format(time=time_now, price=sell_price, cl=closings[-1]))
        else:
            buy_price = driver.get_curr_buy_price()
            if buy_price < ema_ref.values[-1]:
                driver.buy()
                print('Sold at time {time} with buy price {price} and closings {cl}'.format(time=time_now, price=buy_price, cl=closings[-1]))
    time.sleep(9)
 

'''