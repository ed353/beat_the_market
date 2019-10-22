import pandas as pd

#%%
def preprocess_dates(df):
    date_col = df['Date']
    f = lambda x: x.split(' as of ')[0]
    df['Date'] = date_col.map(f)

    df['Date'] = pd.to_datetime(df['Date'])


#%%
df = pd.read_csv('data/play_money_Transactions_20191022-124807.CSV', header=1)
preprocess_dates(df)

option_trades = df.loc[df.Symbol.str.contains('[0-9]{2}/[0-9]{2}/[0-9]{4}').fillna(value=False)]

#%%
amounts = option_trades.Amount.replace('[\$,]', '', regex=True).astype(float)
total_gain = amounts.sum()
total_spent = -amounts[amounts<0].sum()
#%%
print(total_gain)
print(100*total_gain/total_spent)

#%% manual determination of unrealized gain/loss
unrealized_gain = total_gain + 107.87 + 725
print(unrealized_gain)
print(100*unrealized_gain/total_spent)

#%% TODO: find options that were exercised, track the subsequent purchase and sale of the underlying
