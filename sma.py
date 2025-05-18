'''
Simple Moving Average (SMA) Crossover Strategy
By: Pranith Mahanti 
'''

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Required for evading the YFRateLimitError
# Refer: https://github.com/ranaroussi/yfinance/issues/2422#issuecomment-2840774505
from curl_cffi import requests

# Fetch data from Yahoo Finance API
def fetchData(symbol):
    '''
    Return data format:
    Close | High | Low | Open | Volume
    '''
    session = requests.Session(impersonate="chrome")
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="6mo")
    print(data)
    return data['Close'], data['High'], data['Low'], data['Open'], data['Volume']

# Clean Data
def cleanData(data):
    data = data.ffill().bfill() #Forward Fill and Back Fill empty cells
    return data

# Calculate SMAs
def calcSMA(close, win1, win2):
    sma_small = close.rolling(window=win1).mean()
    sma_large = close.rolling(window=win2).mean()

    return sma_small, sma_large

# Buy and Sell Signals
def generateSignals(sma_small, sma_large):
    buy = []
    sell = []
    buy_signals = []
    sell_signals = []

    for i in range(1, len(sma_small)):
        if pd.isna(sma_small.iloc[i-1]) or pd.isna(sma_large.iloc[i-1]):
            continue

        prev_small = sma_small.iloc[i-1]
        prev_large = sma_large.iloc[i-1]
        curr_small = sma_small.iloc[i]
        curr_large = sma_large.iloc[i]

        if prev_small < prev_large and curr_small > curr_large:
            buy.append(close.index[i])
            buy_signals.append(close.iloc[i])
        elif prev_small > prev_large and curr_small < curr_large:
            sell.append(close.index[i])
            sell_signals.append(close.iloc[i])

    return buy, buy_signals, sell, sell_signals


# Run
if __name__ == "__main__":
    close, high, low, open, volume = fetchData('BAJFINANCE.NS')
    close = cleanData(close)
    sma_5, sma_20 = calcSMA(close=close, win1=5, win2=20)
    buy, buy_values, sell, sell_values = generateSignals(sma_small=sma_5, sma_large=sma_20)

    # Plotting graphs
    plt.figure(figsize=(14, 7))
    plt.plot(close, label='Close Price', alpha=0.6)
    plt.plot(sma_5, label='5-Day SMA', linestyle='--')
    plt.plot(sma_20, label='20-Day SMA', linestyle='--')

    plt.scatter(buy, buy_values, marker='^', color='g', label='Buy Signal', s=100)
    plt.scatter(sell, sell_values, marker='v', color='r', label='Sell Signal', s=100)

    plt.title("SMA Crossover Strategy")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
