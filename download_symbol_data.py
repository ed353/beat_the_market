# Download stock information from each of the symbols in the latest
# symbol list

import os
import glob
import random
from time import sleep
import json

from lxml import html
import requests

from collections import OrderedDict

#%%
def get_summary_data(ticker):

    # parse from main quote page
    url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
    response = requests.get(url, verify=False)
    # print ("Parsing %s"%(url))

    sleep(3)

    parser = html.fromstring(response.text)
    summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
    summary_data = OrderedDict()

    # get other details from secondary link
    other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
    summary_json_response = requests.get(other_details_json_link)

    try:
        json_loaded_summary =  json.loads(summary_json_response.text)
        roa = json_loaded_summary['quoteSummary']['result'][0]['financialData']['returnOnAssets']
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

        summary_data.update({'Return on Assets': roa})
        return summary_data

    except:
        print ("Failed to parse json response")
        return {"error": "Failed to parse JSON response."}

#%%
symbol_lists = glob.glob('symbol_list_*.txt')
symbol_lists.sort()
symbol_list_txt_file = symbol_lists[-1]

with open(symbol_list_txt_file, 'r') as f:
    symbols = f.readlines()

symbols = [s.rstrip('\n') for s in symbols]

#%% download financial data from URLs
for idx, symbol in enumerate(symbols):
    print('Downloading information for {}'.format(symbol))
    ticker = symbol.lower()
    output_json = os.path.join('/home/emily/data/btm', '{}.json'.format(ticker))

    if os.path.exists(output_json):
        continue

    summary_data = get_summary_data(ticker)

    with open(output_json, 'w') as f:
        json.dump(summary_data, f)

    if idx % 10 == 0 and idx > 0:
        sleep(random.randint(10, 20))
