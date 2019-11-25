import pandas as pd
from datetime import datetime

#%%
def preprocess_dates(df):
    date_col = df['Date']
    f = lambda x: x.split(' as of ')[0]
    df['Date'] = date_col.map(f)

    df['Date'] = pd.to_datetime(df['Date'])


#%%
# TODO: get latest csv from data directory
df = pd.read_csv('data/play_money_Transactions_20191124-193624.CSV', header=1)
preprocess_dates(df)

df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)
df['Amount'] = df['Amount'].replace('[\$,]', '', regex=True).astype(float)

#%%
option_trades = df.loc[df.Symbol.str.contains('[0-9]{2}/[0-9]{2}/[0-9]{4}').fillna(value=False)]

#%%
amounts = option_trades['Amount']
total_gain = amounts.sum()
total_spent = -amounts[amounts<0].sum()

#%%
print(total_gain)
print(100*total_gain/total_spent)

# TODO: can the values of held positions be determined and then added to the unrealized gain?
#%% TODO: find options that were exercised, track the subsequent purchase and sale of the underlying
exercises = df.loc[df['Action'] == 'Exchange or Exercise']

exercise_symbols = exercises['Symbol'].to_list()

print(exercises)
print(exercise_symbols)

#%%
def parse_option_symbol(option_symbol):
    symbol, date, strike_price, strategy = option_symbol.split(' ')
    date = datetime.strptime(date, '%m/%d/%Y')
    strike_price = float(strike_price)

    return symbol, date, strike_price, strategy



#%% TODO: loop over all exercises
def get_exercise_amount(exercise, all_transactions_df):

    # assert len(exercise) == 1

    ex_sym = exercise['Symbol'] # .values[0]
    option_purchase = all_transactions_df.loc[all_transactions_df['Symbol'] == ex_sym].loc[all_transactions_df['Action'] != 'Exchange or Exercise']
    amount_paid = option_purchase['Amount'].to_list()[0]

    symbol, date, strike, strategy = parse_option_symbol(ex_sym)

    num_contracts = option_purchase['Quantity'].to_list()[0]
    buy_total = strike * num_contracts * 100

    # confirm buy total with subsequent trade
    exercise_purchase = df.iloc[0:(option_purchase.index[0])].loc[df['Symbol'] == symbol].loc[df['Price'] == strike]

    assert exercise_purchase['Amount'].to_list()[-1] == -buy_total

    return -buy_total

#%%
for k in range(len(exercises)):
    print(get_exercise_amount(exercises.iloc[k], df))

#%% TODO: find subsequent sell (or position) and subtract

#%% TODO: loop over all exercises and sum
total_gain += -1020
total_gain += 107
print(total_gain)
print(total_spent)

print(total_gain/11406)
