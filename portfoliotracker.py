'''
Portfolio Tracker
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
    data = ticker.history(period="30d", auto_adjust=False)
    
    return data['Adj Close']

# Clean Data
def cleanData(data):
    data = data.ffill().bfill() # Forward Fill and Back Fill empty cells
    return data

# Calculate Total Portfolio Value
def calculateTotalPortfolio(data, portfolio):
    total = {}
    for i in data:
        prices = []
        stock = data[i]
        for price in stock.iloc:
            prices.append(price*portfolio[stock.name])
        
        total.update({
            stock.name: prices
        })

    return total
        
def calculateTotalValue(data):
    li = [i for i in data.values()]

    df = pd.DataFrame(li)

    return df.sum()


# Run
if __name__ == "__main__":
    portfolio = {
        "INFY.NS": 15,
        "JIOFIN.NS": 10,
        "RELIANCE.NS": 12,
        "HDFCBANK.NS": 15,
        "ABCAPITAL.NS": 7,
    }

    data = cleanData(fetchData(list(portfolio.keys())))
    dates = pd.to_datetime(data.index) #Dates of the Prices
    total = calculateTotalPortfolio(data=data, portfolio=portfolio)
    
    total_values = calculateTotalValue(total)

    # Printing the latest total portfolio value
    print(f'Latest Total Value of the Portfolio: {total_values.iloc[-1]}')

    total_df = pd.Series(total_values)
    total_df.index = dates

    # Plotting graphs
    plt.figure(figsize=(14, 7))
    plt.plot(total_df, label='Total value', alpha=1, color="darkviolet")

    plt.title("Portfolio Tracker")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    
    # Saving the plot as a JPEG file
    plt.savefig("outputs/portfoliotracker.jpg")

    # Showing the plot
    plt.show()
    
