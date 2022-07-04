# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 13:28:32 2022

@author: reece
"""
import requests

url = 'https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_LRC_USD/history?period_id=1DAY&time_start=2018-01-01T00:00:00&time_end=2020-12-31T00:00:00&limit=2000'
#headers = {'X-CoinAPI-Key' : 'F7F21667-42EE-466D-B32D-DB4E2D15E9EE'}
headers = {'X-CoinAPI-Key' : '8C728603-6D0B-45CF-87CE-5D56F7D95BC8'}
r = requests.get(url, headers=headers)
data = r.json()
print(data)

