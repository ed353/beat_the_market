# script to determine how dividend payouts change with the price of a stock,
# and how it affects the yield for a selection of stocks

#%%
import yfinance as yf
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

#%%
symbol = 'MFA'

ticker = yf.Ticker(symbol)
div_data = ticker.dividends

div_dates = div_data.index

min_date = div_dates.min()
max_date = div_dates.max()

price_data = yf.download(symbol, start=min_date, end=max_date)

closes = price_data['Close']
close_dates = price_data.index

#%%
fig = plt.figure(figsize=(10,5))
plt.plot(close_dates, closes)
fig = plt.figure(figsize=(10,5))
plt.scatter(div_dates, div_data)

#%%
# TODO: make data less noisy by averaging over the previous quarter before the dividend
close_on_dividends = price_data.loc[div_dates]['Close']
dividend_percents = 100 * 4 * div_data / close_on_dividends

fig = plt.figure(figsize=(10,5))
_ = plt.scatter(div_dates, dividend_percents)

#%%
closing_prices = price_data['Close']
div_dates
