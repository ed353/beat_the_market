import os

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

from ingest_csv import preprocess_dates

#%%
prices_dir = 'prices'

if not os.path.exists(prices_dir):
    os.makedirs(prices_dir)

#%%
df = pd.read_csv('play_money_Transactions_20190914-162551.CSV', header=1)
preprocess_dates(df)
dates = df['Date']

min_date = dates.min()
max_date = dates.max()

#%%
import yfinance as yf

# Get the data for the stock Apple by specifying the stock ticker, start date, and end date
data = yf.download('AAPL', dates.min(), dates.max())

# Plot the close prices
import matplotlib.pyplot as plt
data.Close.plot()
plt.show()

#%%
symbols = list(set(list(df['Symbol'])))

for sym in symbols:

    try:
        data = yf.download(sym, min_date, max_date)
        fn = os.path.join(prices_dir, sym + '.csv')

        data.to_csv(fn)
    except:
        print(sym)


#%%
df.loc[df['Symbol'] == 'YECO']
