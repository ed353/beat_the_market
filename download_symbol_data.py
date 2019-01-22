# Download stock information from each of the symbols in the latest
# symbol list

import os
import glob
import random
from time import sleep
import json
from lxml import html

from collections import OrderedDict

from scraping import Scraper

#%%
import warnings
warnings.filterwarnings("ignore")


#%%
def request_main_quote(scraper, ticker):
    url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
    response = scraper.get_request(url, verify=False)
    return response

def request_other_details(scraper, ticker):
    url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
    response = scraper.get_request(url)
    return response

#%%
def get_summary_data(scraper, ticker):

    main_response = request_main_quote(scraper, ticker)
    sleep(2)

    parser = html.fromstring(main_response.text)
    summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
    summary_data = OrderedDict()

    # get other details from secondary link
    summary_json_response = request_other_details(scraper, ticker)

    try:
        json_loaded_summary =  json.loads(summary_json_response.text)
        roa = json_loaded_summary['quoteSummary']['result'][0]['financialData']['returnOnAssets']
        earnings_list = json_loaded_summary["quoteSummary"]["result"][0]["calendarEvents"]['earnings']
        datelist = []

        for i in earnings_list['earningsDate']:
            datelist.append(i['fmt'])
        earnings_date = ' to '.join(datelist)

        for table_data in summary_table:
            raw_table_key = table_data.xpath('.//td[contains(@class,"C(black)")]//text()')
            raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()')
            table_key = ''.join(raw_table_key).strip()
            table_value = ''.join(raw_table_value).strip()
            summary_data.update({table_key:table_value})

        summary_data.update({'Return on Assets': roa, 'Earnings Date': earnings_date})
        return summary_data

    except:
        print ("Failed to parse json response")
        return None


#%% get list of symbols to download
symbol_lists = glob.glob('symbol_list_*.txt')
symbol_lists.sort()
symbol_list_txt_file = symbol_lists[-1]

with open(symbol_list_txt_file, 'r') as f:
    symbols = f.readlines()

symbols = [s.rstrip('\n') for s in symbols]

#%% initialize a scraper
scraper = Scraper()

#%% download financial data from URLs
for idx, symbol in enumerate(symbols):
    ticker = symbol.lower()
    output_json = os.path.join('/home/emily/data/btm', '{}.json'.format(ticker))

    if os.path.exists(output_json):
        continue

    print('Downloading information for {}'.format(symbol))
    summary_data = get_summary_data(scraper, ticker)

    if summary_data is not None:
        with open(output_json, 'w') as f:
            json.dump(summary_data, f)

    if idx % 10 == 0 and idx > 0:
        sleep(random.randint(5, 10))
