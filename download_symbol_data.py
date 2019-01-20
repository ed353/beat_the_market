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

    # TODO: move requests to separate function
    # parse from main quote page
    url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
    # response = requests.get(url, verify=False)
    response = get_request(url, verify=False)
    # print ("Parsing %s"%(url))

    sleep(3)

    parser = html.fromstring(response.text)
    summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
    summary_data = OrderedDict()

    # get other details from secondary link
    other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
    # summary_json_response = requests.get(other_details_json_link)
    summary_json_response = get_request(other_details_json_link)

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

#%%
def get_proxies():
    ''' Grab a list of 10 elite proxies from free-proxy-list.net
    '''
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = html.fromstring(response.text)
    proxies = set()
    n_proxies = 0
    i_proxy = 0

    while n_proxies < 10:
        i = parser.xpath('//tbody/tr')[i_proxy]
        if i.xpath('.//td[5][contains(text(),"elite")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
            n_proxies += 1
        i_proxy += 1

    return proxies

#%%
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

def get_random_user_agent():
    user_agent = random.choice(user_agent_list)
    #Set the headers
    headers = {'User-Agent': user_agent}
    return headers

#%%
def get_request(url, **kwargs):
    ''' Wrapper for request.get using a random proxy and user agent.
    '''
    headers = get_random_user_agent()
    proxy = random.choice(proxies)
    response = requests.get(url, headers=headers,
        proxies={"http": proxy, "https": proxy},
        **kwargs)
    return response

#%% get list of symbols to download
symbol_lists = glob.glob('symbol_list_*.txt')
symbol_lists.sort()
symbol_list_txt_file = symbol_lists[-1]

with open(symbol_list_txt_file, 'r') as f:
    symbols = f.readlines()

symbols = [s.rstrip('\n') for s in symbols]

#%% get list of proxies to use
proxies = list(get_proxies()) #TODO: refresh list of proxies every 10 minutes

#%% download financial data from URLs
for idx, symbol in enumerate(symbols):
    print('Downloading information for {}'.format(symbol))
    ticker = symbol.lower()
    output_json = os.path.join('/home/emily/data/btm', '{}.json'.format(ticker))

    if os.path.exists(output_json):
        continue

    summary_data = get_summary_data(ticker)

    if summary_data is not None:
        with open(output_json, 'w') as f:
            json.dump(summary_data, f)

    if idx % 10 == 0 and idx > 0:
        sleep(random.randint(10, 20))
