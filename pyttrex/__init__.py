import numpy as np
from urllib.request import urlopen, Request
import json

def ohlc(coin, tickinterval):
    try:
        req = Request('https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={0}&tickInterval={1}'.format(coin, tickinterval))
        response = json.loads(urlopen(req, timeout=2).read().decode())
        candles = {
            'O': np.array([candle['O'] for candle in response['result']]),
            'H': np.array([candle['H'] for candle in response['result']]),
            'L': np.array([candle['L'] for candle in response['result']]),
            'C': np.array([candle['C'] for candle in response['result']]),
            'V': np.array([candle['V'] for candle in response['result']]),
            'T': np.array([candle['T'] for candle in response['result']]),
            'BV': np.array([candle['BV'] for candle in response['result']])
        } if response['success'] else None
        result = { 'name': coin, 'candles': candles }
    except:
        result = { 'name': coin, 'candles': False }
    finally:
        return result

def market_summaries(coins=['BTC','ETH']):
    from urllib.request import Request, urlopen
    import json
    url = Request('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    result = json.loads(urlopen(url).read().decode())
    if result['success']:
        return [m['MarketName'] for m in result['result'] if m['MarketName'][:3] in coins]