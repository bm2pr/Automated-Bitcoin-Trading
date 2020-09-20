import numpy, pandas, requests, json, csv, time, Config
from datetime import datetime
from Driver import Driver
#import matplotlib
#matplotlib.use('WXAgg')
import matplotlib.pyplot as plot
from EMA import ExponentialMovingAverage
from dateutil import parser


def get_data():
    driver = Driver()
    driver.login_method()

    buy_price_csv = open('BuyPrice.csv', 'w', newline='')
    sell_price_csv = open('SellPrice.csv', 'w', newline='')
    mark_price_csv = open('MarketPrice.csv', 'w', newline='')

    buy_writer = csv.writer(buy_price_csv)
    buy_writer.writerow(['Time', 'Buy Price'])
    sell_writer = csv.writer(sell_price_csv)
    sell_writer.writerow(['Time', 'Sell Price'])
    mark_writer = csv.writer(mark_price_csv)
    mark_writer.writerow(['Time', 'Market Price'])

    while True:
        bp = driver.get_curr_buy_price()
        buy_writer.writerow([datetime.now(), bp])
        sp = driver.get_curr_sell_price()
        sell_writer.writerow([datetime.now(), sp])
        mp = driver.get_curr_market_price()
        if not mp == 0:
            mark_writer.writerow([datetime.now(), mp])
        time.sleep(0.5)

get_data()