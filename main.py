# Modules
import yfinance as yf
import numpy as np
from scipy.optimize import minimize
from tabulate import tabulate
from datetime import datetime
import argparse

# Test input
# python main.py --stocks 'PG KO MSFT JPM PG BRK-B PEP VZ PFE COST' --investment 10000 --conf 90

# CVaR Objective function
def CVaR(x):

    # Extracting weights and v separately
    w = x[:-1]
    v = x[-1]

    N = trimmed_returns.shape[0]
    SUM = 0

    # Objective Monte carlo
    for i in range(N):
        sample = trimmed_returns[i]
        var_excess = max(-np.dot(w, sample) - v, 0)
        SUM += var_excess
    
    return v + (SUM / ((1 - ALPHA) * N))

# Argument parser
parser = argparse.ArgumentParser()

# Adding and parsing arguments
parser.add_argument('--stocks', type=str, help="Ticker Symbol (Stock)", required=True)
parser.add_argument('--investment',  type=float, help="Investment Amount", required=True)
parser.add_argument('--conf', type=float, help="Confidence Percentage", required=True)
args = parser.parse_args()

# Obtaining and handling arguments
tickers = args.stocks.split(" ")
INVEST = args.investment
ALPHA = args.conf / 100

# Declaring optimizer constants and arguments
# V is appended into WEIGHTS to optimize equally
V = 1
WEIGHTS = np.full(len(tickers), 1/len(tickers))
x0 = np.append(WEIGHTS, V)

# Fetching
# Obtaining data from 2023 until now
now = datetime.now().strftime("%Y-%m-%d")
data = yf.download(tickers, start="2023-01-01", end=now, interval='1d', group_by='ticker', auto_adjust=True)

# Structuring
# Formatting data into return matrix
returns_list = []
for i in tickers:
    stock_returns = data[i]["Close"].pct_change().dropna().values
    returns_list.append(stock_returns)

# Failsafe
# Detecting the asset having minimum frequency of returns and truncating past data for every other assets
# Prevents the optimizer from tweaking and makes the optimizing fair
minLen = min(len(x) for x in returns_list)
trimmed_returns = np.array([r[-minLen:] for r in returns_list]).T

# Objective
# Minimizing function and obtaining optimized weights
res = minimize(CVaR, x0, method='SLSQP', bounds=[(0,1)]*len(WEIGHTS) + [(None,None)], constraints= [{'type':'eq','fun': lambda x: x[:-1].sum()-1}])
optimized_weights = [round(x, 4) for x in res.x[:-1]]

# Eye candy
# Using tables to display adequate data nicely
optimized_investments = [round(x*INVEST, 2) for x in optimized_weights]
short_lived_array = [tickers, optimized_weights, optimized_investments]
table = [[short_lived_array[0][i], short_lived_array[1][i], short_lived_array[2][i]] for i in range(len(optimized_weights))]
table.append(["TOTAL", sum(optimized_weights), sum(optimized_investments)])

print(tabulate(table, headers=["STOCK", "WEIGHT", "INVESTMENT"], tablefmt='plain'))