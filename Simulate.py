import matplotlib.pyplot as plot
import dateutil.parser
import time
import json, pandas, numpy, seaborn, scipy
from EMA import ExponentialMovingAverage
from datetime import datetime, timedelta

# Main test function for determining if it will go up
def plot_ema_roc_hst(curr_df, **kwargs):
    for key, value in kwargs.items():
        if key == 'hour':
            curr_df = curr_df.loc[curr_df.index.hour == value]
    ema_1 = curr_df.ewm(span=344).mean()
    ema_1_diff = ema_1.diff()
    ema_roc_list = []
    curr_time = ema_1_diff.first_valid_index()
    last_time = ema_1_diff.last_valid_index()
    plot.show()
    while curr_time < last_time:
        closest_index = ema_1_diff.index.get_loc(curr_time, method='nearest')
        curr_ema_price_diff = ema_1_diff.iloc[closest_index].iat[0]
        curr_ema_time = ema_1_diff.iloc[closest_index].name
        prev_ema_time = ema_1_diff.iloc[closest_index-1].name
        time_diff = curr_ema_time - prev_ema_time
        time_diff_sec = time_diff.seconds + time_diff.microseconds / 1000000
        ema_roc = curr_ema_price_diff / time_diff_sec
        ema_roc_list.append(ema_roc)
        curr_time = curr_time + timedelta(seconds=1)
    
    seaborn.distplot(ema_roc_list, bins=50, hist=True, kde=True, label='EMA 200 Rate of Change Distribution')
    plot.show()
    

def plot_data(buy_df, sell_df, time, ema):
    hour_ago = time - timedelta(hours=1)
    plot.plot(sell_df.loc[(sell_df.index > hour_ago) & (sell_df.index <= time)], color='red', label='Sell Price')
    plot.plot(buy_df.loc[(buy_df.index > hour_ago) & (buy_df.index <= time)], color='green', label='Buy Price')
    colors = ['black', 'purple', 'blue', 'orange']
    color_ind = 0
    for span in ema:
        ema = sell_df.loc[(sell_df.index > hour_ago) & (sell_df.index <= time)].ewm(span=span).mean()
        plot.plot(ema, color=colors[color_ind], label='EMA {sp} Past Hour'.format(sp=span))
        color_ind = color_ind + 1

    # Plot the legend and show the graph - requires valid backend to show
    plot.legend()
    plot.show()

def get_data(date):
    buy_df = pandas.read_csv('RobinhoodData/' + date + '/BuyPrice.csv', index_col=0, parse_dates=True)
    sell_df =  pandas.read_csv('RobinhoodData/' + date + '/SellPrice.csv', index_col=0, parse_dates=True)
    
    return buy_df, sell_df
 
def ema_roc(df, span, curr_time):
    hour_ago = curr_time - timedelta(hours=1)
    # Calculate Exponential Moving Average for last hour
    ema = df.loc[(df.index > hour_ago) & (df.index <= curr_time)].ewm(span=span).mean()
    # Make dataframe into changes of exponential moving averages
    ema_diff = ema.diff()
    # Find the most recent price difference available
    closest_index = ema_diff.index.get_loc(curr_time, method='pad')
    curr_ema_price_diff = ema_diff.iloc[closest_index].iat[0]
    # Find the difference in time that occurred with that price difference
    curr_ema_time = ema_diff.iloc[closest_index].name
    prev_ema_time = ema_diff.iloc[closest_index-1].name
    time_diff = curr_ema_time - prev_ema_time
    time_diff_sec = time_diff.seconds + time_diff.microseconds / 1000000
    #print(time_diff_sec)
    # Calculate the rate of change of that price difference
    curr_ema_roc = curr_ema_price_diff / time_diff_sec
    return curr_ema_roc

def ema_roc_z_score(df, span, curr_time):
    start_time = curr_time - timedelta(minutes=20)
    # Calculate Exponential Moving Average for last hour
    ema = df.loc[(df.index > start_time) & (df.index <= curr_time)].ewm(span=span).mean()
    # Make dataframe into changes of exponential moving averages
    ema_diff = ema.diff()
    # Store all rate of changes in a list
    ema_roc_list = []
    start_time = start_time + timedelta(seconds=2)
    while start_time <= curr_time:
        # Find the most recent index and the changed ema from the previous index
        closest_index = ema_diff.index.get_loc(start_time, method='pad')
        curr_ema_price_diff = ema_diff.iloc[closest_index].iat[0]
        # Find the difference in time that occured
        curr_ema_time = ema_diff.iloc[closest_index].name
        prev_ema_time = ema_diff.iloc[closest_index-1].name
        time_diff = curr_ema_time - prev_ema_time
        time_diff_sec = time_diff.seconds + time_diff.microseconds / 1000000
        # Use the changed ema and the time difference to calculate rate of change
        ema_roc = curr_ema_price_diff / time_diff_sec
        ema_roc_list.append(ema_roc)
        start_time = start_time + timedelta(seconds=1)
    z_scores = scipy.stats.zscore(ema_roc_list, nan_policy='omit')
    print(z_scores)
    return z_scores[len(z_scores) - 1]

def ema_gap(df, span, curr_time):
    hour_ago = curr_time - timedelta(hours=1)
    ema = df.loc[(df.index > hour_ago) & (df.index <= curr_time)].ewm(span=span).mean()
    # Find most recent index for current time 
    closest_df_index = df.index.get_loc(curr_time, method='pad')
    closest_ema_index = ema.index.get_loc(curr_time, method='pad')
    # Use index to get ema value and price value
    curr_prc = df.iloc[closest_df_index].iat[0]
    curr_ema = ema.iloc[closest_ema_index].iat[0]
    return curr_prc - curr_ema

def find_price(df, curr_time):
    index = df.index.get_loc(curr_time, method='nearest')
    return df.iloc[index].iat[0]

def run_sim(date, show_sim_steps, span, ref_buy_ema_roc, ref_sell_gap):
    buy_df, sell_df = get_data(date)
    # Initialize values
    bought = False
    curr_time = buy_df.iloc[120].name
    last_time = buy_df.last_valid_index()
    last_buy_price = 0
    amount = 10
    num_trades = 0
    while curr_time <= last_time:
        if not bought:
            buy_ema_roc = ema_roc(buy_df, span, curr_time)
            if buy_ema_roc <= ref_buy_ema_roc:
                bought = True
                last_buy_price = find_price(buy_df, curr_time)
                num_trades = num_trades + 1
                if show_sim_steps:
                    print('Bought at {t} with ema gap {eg}, current amount is now ${amt}'.format(t=curr_time, eg=buy_ema_roc, amt=amount))
                    plot_data(buy_df, sell_df, curr_time, [span, 2000])
        elif bought:
            sell_ema_gap = ema_gap(sell_df, span, curr_time)
            if sell_ema_gap > ref_sell_gap:
                bought = False
                curr_sell_price = find_price(sell_df, curr_time)
                # How much money we made is based upon the percent change from the last time we bought
                amount = amount + ( (curr_sell_price - last_buy_price) / last_buy_price ) * amount
                num_trades = num_trades + 1
                if show_sim_steps:
                    print('Sold at {t} with ema gap {eg}, current amount is now ${amt}'.format(t=curr_time, eg=sell_ema_gap, amt=amount))
                    plot_data(buy_df, sell_df, curr_time, [span, 320])

        curr_time = curr_time + timedelta(seconds=1)
    # Wrap things up by accounting for the value we have in bitcoin
    if bought:
        curr_sell_price = find_price(sell_df, curr_time)
        # How much money we made is based upon the percent change from the last time we bought
        amount = amount + ( (curr_sell_price - last_buy_price) / last_buy_price ) * amount
    return amount

def run_sim_z_scores(date, show_sim_steps, span, buy_z, sell_z):
    buy_df, sell_df = get_data(date)
    # Initialize values
    bought = False
    curr_time = buy_df.iloc[200].name
    last_time = buy_df.last_valid_index()
    last_buy_price = 0
    amount = 10
    num_trades = 0
    while curr_time <= last_time:
        if not bought:
            curr_z = ema_roc_z_score(buy_df, span, curr_time)
            if curr_z <= buy_z:
                bought = True
                last_buy_price = find_price(buy_df, curr_time)
                num_trades = num_trades + 1
                if show_sim_steps:
                    print('Bought at {t} with ema gap {eg}, current amount is now ${amt}'.format(t=curr_time, eg=buy_ema_roc, amt=amount))
                    plot_data(buy_df, sell_df, curr_time, [span, 2000])
        elif bought:
            curr_z = ema_roc_z_score(sell_df, span, curr_time)
            if curr_z > sell_z:
                bought = False
                curr_sell_price = find_price(sell_df, curr_time)
                # How much money we made is based upon the percent change from the last time we bought
                amount = amount + ( (curr_sell_price - last_buy_price) / last_buy_price ) * amount
                num_trades = num_trades + 1
                if show_sim_steps:
                    print('Sold at {t} with ema gap {eg}, current amount is now ${amt}'.format(t=curr_time, eg=sell_ema_gap, amt=amount))
                    plot_data(buy_df, sell_df, curr_time, [span, 320])

        curr_time = curr_time + timedelta(seconds=1)
    # Wrap things up by accounting for the value we have in bitcoin
    if bought:
        curr_sell_price = find_price(sell_df, curr_time)
        # How much money we made is based upon the percent change from the last time we bought
        amount = amount + ( (curr_sell_price - last_buy_price) / last_buy_price ) * amount
    return amount

def test_sim():
    #output_file = open('sim_results_ema_gap_method.txt', 'a')
    test_data = [
        [344, -1.4, 1.2]
    ]
    for x in test_data:
        result_1 = run_sim_z_scores('May31', True, x[0], x[1], x[2])
        print(result_1)
        #output_file.write(result_1 + '\n')
        #output_file.write(result_2 + '\n')
        #output_file.write('\n')
    

#b, s = get_data('May31')
#curr_time = datetime(2020, 5, 31, 10, 41, 11)
#plot_data(b, s, curr_time, [8, 13, 34, 55])
#test_model_independent_of_input_num()
#short_long_ema()
#run_sim(False)
'''
b, s = get_data('June02')
plot_ema_roc_hst(b, hour=9)
plot_ema_roc_hst(b, hour=10)
'''
#test_sim()
#last_time = b.last_valid_index()
#plot_data(b, s, last_time, [744, 5000])
print(run_sim('June02', True, 144, -0.49, 20))
#plot_ema_roc_hst(b)
#test_sim()
