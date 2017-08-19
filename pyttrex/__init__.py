import numpy as np
import pandas as pd
from urllib.request import urlopen, Request
from multiprocessing.pool import ThreadPool
import json
import time, random

def ohlc(*args, **kwargs):
    coin = args[0]
    tickinterval = args[1]
    url = 'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={0}&tickInterval={1}'.format(coin, tickinterval)
    try:
        req = Request(url)
        response = json.loads(urlopen(req, timeout=5).read().decode())
    except:
        time.sleep(random.randint(3, 7))
        try:
            req = Request(url)
            response = json.loads(urlopen(req, timeout=5).read().decode())
        except:
            raise TimeoutError("cant get candles from trex")

    candles = {
        'open': np.array([candle['O'] for candle in response['result']]),
        'high': np.array([candle['H'] for candle in response['result']]),
        'low': np.array([candle['L'] for candle in response['result']]),
        'close': np.array([candle['C'] for candle in response['result']]),
        'time': np.array([candle['T'] for candle in response['result']]),
        'volume': np.array([candle['BV'] for candle in response['result']])
    } if response['success'] else None
    dataframe = pd.DataFrame(candles) if candles else None
    if dataframe is not None:
        dataframe = dataframe.set_index(pd.to_datetime(dataframe['time']))
        return {'name': coin, 'data': dataframe }
    else:
        return None

def market_summaries(coins=['BTC','ETH'], filtered=False):
    from urllib.request import Request, urlopen
    import json
    url = Request('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    result = json.loads(urlopen(url).read().decode())
    exceptionlist = [ 'WAVES' ] #''LSK', 'BNT', 'PIVX', 'LBC', 'WINGS', 'PTOY', 'NMR', 'XEM', 'WAVES', 'BTS', 'SC', 'DASH', 'FCT', 'SNT', 'STORJ', 'GBYTE', '1ST', 'DGB', 'ARDR', 'NXT', 'VIA', 'SEQ' ]
    if result['success']:
      if filtered:
        return [ m['MarketName'] for m in result['result'] if m['MarketName'][:3] in coins and m['BaseVolume'] >= 1000 or m['MarketName'].split("-")[0] in coins and m['MarketName'].split("-")[1] in exceptionlist ]
      else:
        return [m['MarketName'] for m in result['result'] if m['MarketName'][:3] in coins]

def market_candles(market, tickinterval):
    pool = ThreadPool(processes=16)
    async_result = [ pool.apply_async(ohlc, (coin, tickinterval)).get() for coin in market ]
    return async_result