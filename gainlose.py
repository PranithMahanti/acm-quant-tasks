'''
Gainers Losers Strategy
By: Pranith Mahanti 
'''

import random
import csv 

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Required for evading the YFRateLimitError
# Refer: https://github.com/ranaroussi/yfinance/issues/2422#issuecomment-2840774505
from curl_cffi import requests

# To pick random companies from the NIFTY 50 List
def getRandomSybmols(n=20):
    '''
    Selects random companies from the given csv file

    Args:
    n (int): Number of companies to select (Default: 20)

    Returns:
    Pandas DataFrame Object of the selected list of companies
    '''

    data = pd.read_csv("nifty50list.csv")
    li = random.sample(range(1, 21), n)

    companies = []

    for num in li:
        companies.append(data.iloc[num])

    return pd.DataFrame(data=companies)

# Fetch data from Yahoo Finance API
def fetchData(symbols):
    '''
    Returns:
    Pandas DataFrame Object of the adjusted closing prices
    '''
    session = requests.Session(impersonate="chrome")
    ticker = yf.Tickers(symbols, session=session)
    data = ticker.history(period="1mo", auto_adjust=False)
    
    return data['Adj Close']

# Clean Data
def cleanData(data):
    data = data.ffill().bfill() #Forward Fill and Back Fill empty cells
    return data

# Calculate Percentage Loss/Profit Percentages
def calculatePercents(data):
    change = {}
    for i in data:
        stock = data[i]
        first_day = stock.iloc[0]
        last_day = stock.iloc[-1]

        percent_change = ((last_day-first_day)/(first_day))*100
        
        change.update({str(stock.name): float(percent_change)})

    return change

# Sort Dictionary
def sort_dict(dictionary):
    sorted_dict = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}

    return sorted_dict

# Run
if __name__ == "__main__":
    # Selecting 20 random companies from the NIFTY 50 List
    companies = getRandomSybmols()

    # Adding .NS at the end of symbols because YFinance API recognises Indian stocks with .NS at the end
    symbols = [symbol+'.NS' for symbol in companies['Symbol'].to_list()]

    print("Selected 20 Companies from Nifty 50:")
    for company in companies['Company Name']:
        print(company)

    data = cleanData(fetchData(symbols=symbols))
    change = calculatePercents(data=data)

    # Sorting based on the percent changes
    change = sort_dict(change)

    # Identifying Top Gainers and Top Losers
    top_gainers = dict(list(change.items())[:5])
    top_losers = dict(list(change.items())[-5:])

    # Saving to a CSV file
    fieldnames = ["Stock Symbol", "Percent Change"]

    percent_list = [{"Stock Symbol": i, "Percent Change": change[i]} for i in change]

    with open("percent_change.csv", mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(percent_list) 

    # Plotting graphs
    plt.figure(figsize=(14, 7))
    #plt.barh(list(top_gainers.keys())+list(top_losers.keys()), list(top_gainers.values())+list(top_losers.values()),
    #         color="darkviolet")
    plt.barh(list(top_gainers.keys()), list(top_gainers.values()), color="green")
    plt.barh(list(top_losers.keys()), list(top_losers.values()), color="red")
    plt.title("Top Gainers and Losers")
    plt.xlabel("Percentage Change")
    plt.ylabel("Stock Symbol")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    
