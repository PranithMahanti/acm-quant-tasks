'''
Rolling Statistics and Volatility Analysis
By: Pranith Mahanti 
'''

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Required for evading the YFRateLimitError
# Refer: https://github.com/ranaroussi/yfinance/issues/2422#issuecomment-2840774505
from curl_cffi import requests

# Fetch data from Yahoo Finance API
def fetchData(symbols):
    '''
    Returns:
    Pandas DataFrame Object of the adjusted closing prices
    '''
    session = requests.Session(impersonate="chrome")
    ticker = yf.Tickers(symbols, session=session)
    data = ticker.history(period="6mo")
    
    return data['Close']

# Clean Data
def cleanData(data):
    data = data.ffill().bfill() # Forward Fill and Back Fill empty cells
    return data

# Calculate Daily Percentage Changes (Daily returns) in Closing prices
def calculateDailyPercents(close):
    change = []
    for i in range(1, len(close)):
        percent_change = ((close.iloc[i]-close.iloc[i-1])/close.iloc[i-1])*100
        change.append(percent_change)

    return change

# Calculate Rolling Averages and Standard Deviations of Daily Returns
def calculateRolling(change_df):
    rolling_avg = change_df.rolling(window=7).mean()
    rolling_std = change_df.rolling(window=7).std()

    return rolling_avg, rolling_std

# Run
if __name__ == "__main__":
    close = cleanData(fetchData('RELIANCE.NS'))
    change = calculateDailyPercents(close=close)

    change_df = pd.DataFrame(change)
    change_df.index = close.index[1:]

    rolling_avg, rolling_std = calculateRolling(change_df=change_df)
    rolling_std = rolling_std.dropna() #Dropping Nan Fields
    rolling_avg = rolling_avg.dropna() #Dropping Nan Fields
    
    # Plotting graphs
    plt.figure(figsize=(14, 7))
    plt.plot(change_df, label='Daily Returns')
    plt.plot(rolling_avg, label='Rolling Average', linestyle='--')
    plt.plot(rolling_std, label="Rolling Standard Deviation", linestyle="--")

    plt.title("Rolling Statistics and Volatility Analysis")
    plt.xlabel("Date")
    plt.ylabel("Percents")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
