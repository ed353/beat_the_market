# Download stock information from each of the symbols in the latest
# symbol list

import os
import glob
import random
from lxml import html
import requests
from time import sleep
import json
from collections import OrderedDict

#%%
with open('appl_raw.json', 'r') as f:
    json_txt = f.read()


#%% download financial data from URLs
ticker = 'aapl'
output_json = os.path.join('/home/emily/data/btm', '{}.json'.format(ticker))

# parse from main quote page
url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
response = requests.get(url, verify=False)
print ("Parsing %s"%(url))
sleep(4)
parser = html.fromstring(response.text)
summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
summary_data = OrderedDict()

# get other details from secondary link
other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
summary_json_response = requests.get(other_details_json_link)

#%%
json_loaded_summary =  json.loads(json_txt)
roa = json_loaded_summary['quoteSummary']['result'][0]['financialData']['returnOnAssets']

#%%
try:
    json_loaded_summary =  json.loads(summary_json_response.text)
    # y_Target_Est = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["targetMeanPrice"]['raw']
    # earnings_list = json_loaded_summary["quoteSummary"]["result"][0]["calendarEvents"]['earnings']
    # eps = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']
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

    # summary_data.update({'1y Target Est':y_Target_Est,'EPS (TTM)':eps,'Earnings Date':earnings_date,'ticker':ticker,'url':url})
    summary_data.update({'Return on Assets': roa})

except:
	print ("Failed to parse json response")


#%%
with open(output_json, 'w') as f:
    json.dump(summary_data, f)
