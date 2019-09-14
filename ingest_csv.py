from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

#%%
df = pd.read_csv('play_money_Transactions_20190914-162551.CSV', header=1)

df.iloc[669]

df['Date']
#%%
# Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
tickers = ['AAPL', 'MSFT', '^GSPC']

# We would like all available data from 01/01/2000 until 12/31/2016.
start_date = '2010-01-01'
end_date = '2016-12-31'

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
panel_data = data.DataReader('INPX', 'google', start_date, end_date)

#%%
# Import yfinance
import yfinance as yf

# Get the data for the stock Apple by specifying the stock ticker, start date, and end date
data = yf.download('AAPL','2016-01-01','2019-09-13')

# Plot the close prices
import matplotlib.pyplot as plt
data.Close.plot()
plt.show()
