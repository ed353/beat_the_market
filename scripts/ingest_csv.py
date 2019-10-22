import pandas as pd

#%%
def preprocess_dates(df):
    date_col = df['Date']
    f = lambda x: x.split(' as of ')[0]
    df['Date'] = date_col.map(f)

    df['Date'] = pd.to_datetime(df['Date'])


#%%
df = pd.read_csv('play_money_Transactions_20190914-162551.CSV', header=1)
preprocess_dates(df)

df['Action'].unique()

#%%
deposits = df.loc[df['Action'] == 'MoneyLink Deposit']

deposits

#%%
recv = df.loc[df['Action'] == 'Funds Received']
recv
