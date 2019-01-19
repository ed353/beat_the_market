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
companies_list = companies_list.reset_index(drop=True)
#%%
companies_list.head()

#%% Eliminate foreign companies
is_domestic = companies_list['ADR TSO'].isna()
domestic_idxs = companies_list.index[is_domestic == True].tolist()

domestic_list = companies_list.iloc[domestic_idxs]
domestic_list = domestic_list.reset_index(drop=True)

#%% Eliminate utilities and financial stocks
is_financial = domestic_list['Sector'] == 'Finance'
is_utilities = domestic_list['Sector'] == 'Public Utilities'


sector_idxs = domestic_list.index[~(is_financial | is_utilities)].tolist()
sector_list = domestic_list.iloc[sector_idxs]

#%% Filter stocks with duplicate symbols
