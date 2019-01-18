# Download lists of companies from NYSE, NASDAQ, and AMEX from
# Nasdaq.com and combine them into one Pandas dataframe.

import urllib
import pandas as pd

#%%
NYSE_URL='https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download'
NASDAQ_URL='https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
AMEX_URL='https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=AMEX&render=download'


#%%
nyse_list = pd.read_csv(NYSE_URL)
nasdaq_list = pd.read_csv(NASDAQ_URL)
amex_list = pd.read_csv(AMEX_URL)

#%%
companies_list = pd.concat([nyse_list, nasdaq_list, amex_list], ignore_index=True)
companies_list = companies_list.sort_values('MarketCap', ascending=False)

companies_list.head()
