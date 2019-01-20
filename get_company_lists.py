# Download lists of companies from NYSE, NASDAQ, and AMEX from
# Nasdaq.com and combine them into one Pandas dataframe.

import urllib
import pandas as pd
import datetime

#%%
NYSE_URL='https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download'
NASDAQ_URL='https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
AMEX_URL='https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=AMEX&render=download'
#%%
currdate = datetime.datetime.now()
date_str = str(currdate.year) + str(currdate.month).zfill(2) + str(currdate.day).zfill(2)

OUTPUT_FILENAME='symbol_list_{}.txt'.format(date_str)

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
sector_list = sector_list.reset_index(drop=True)

#%% Filter stocks with duplicate symbols
is_duplicate_name = sector_list.duplicated(subset='Name')
duplicate_idxs = sector_list.index[~is_duplicate_name].tolist()

non_duplicate_list = sector_list.iloc[duplicate_idxs]

non_duplicate_list.head()

#%% Export company symbols to file
symbol_list = non_duplicate_list['Symbol'].tolist()

with open(OUTPUT_FILENAME, 'w') as f:
    for symbol in symbol_list:
        f.write(symbol+'\n')
