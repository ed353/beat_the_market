

def preprocess_dates(transactions_df):
    date_col = transactions_df['Date']
    # some dates have a weird string format, parse the later date for those
    f = lambda x: x.split(' as of ')[0]
    transactions_df['Date'] = date_col.map(f)

    # seomtimes the transaction total is listed in the dates column, if so remove it
    idx = transactions_df.index[transactions_df['Date']=='Transactions Total']
    transactions_df.drop(idx, inplace=True)


def get_latest_data(data_dir='data/'):
    pass


def filter_options_trades(transactions_df):
    pass
