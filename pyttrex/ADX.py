from pyttrex import  market_candles, market_summaries
import pandas as pd
import numpy as np

from talib import EMA,  SMA
buys = []
sells = []
buy_symbols = []
sell_symbols = []
timeperiod = 14

# Get our indicators. We pass this function the needed data.
def get_indicator(df, period):
    # Get money flow index

    ema = EMA(df.close.values, timeperiod = period)
    sma = SMA(df.close.values, timeperiod = period)
    return ema, sma


money = 0.2
total = money
markets = market_summaries(['BTC'], filtered=True)
wallets = [ {'market': x, 'base': 0, 'pair': 0, 'price': 0 } for x in markets ]

for wallet in wallets:
    tick = 0
    market = [ wallet['market'] ]
    candles = market_candles(market, 'FiveMin')

    for c in candles:
        dataframe = c['data']
        dataframe.set_index(pd.to_datetime(dataframe['time']))
        dataframe = dataframe.resample('5T').agg({
            'open': 'first',
            'close': 'last',
            'high': 'max',
            'low': 'min',
            'volume': 'sum',
            'time': 'last'
        })
        threefiddy = dataframe.resample('6H').agg({
            'open': 'first',
            'close': 'last',
            'high': 'max',
            'low': 'min',
            'volume': 'sum',
            'time': 'last'
        })

        ema = EMA(np.array(dataframe.close), timeperiod)
        sma = SMA(np.array(dataframe.close), timeperiod)

        test = zip(ema, sma, dataframe.close, dataframe.high, dataframe.time)
        high = 0
        while True:
            try:
                i = next(test)
                eema, ssma, close, dfhigh, dftime = i[0], i[1], i[2], i[3], i[4]
                if 'n' == str(eema)[0] or 'n' == str(ssma)[0]: continue
                high = dfhigh if dfhigh > high else high
                if dfhigh >= high:
                    if tick <= 5:
                        investment = (money * 1.02) - money
                        money = money - investment
                        if wallet['base'] > 0:
                            investment += wallet['base']
                            wallet['base'] = 0
                            tick += 1
                        tick += 1
                        wallet['pair'] += investment / dfhigh
                        wallet['price'] = float('{0:.8f}'.format((wallet['price'] + dfhigh) / 2))

                exitpos = wallet['price'] * 0.95
                if close <= exitpos:
                    if wallet['pair'] > 0:
                        wallet['base'] += wallet['pair'] * dfhigh
                        wallet['pair'] = 0
                        wallet['price'] = 0
                        tick = 0
            except StopIteration:
                wallet['base'], wallet['pair'] = close * wallet['pair'] if wallet['base'] == 0 else wallet['base'], 0
                break


winners = sorted(wallets, key= lambda x: x['base'])
#for w in winners:
#    print(w)
print("{0:.3f} BTC distributed in total".format(total))
print("{0:.3f} BTC left untouched of original distribution".format(money))
print("{0:.3f} BTC distributed among coinpairs".format(sum([x['base'] for x in wallets])))
print("{0:.3f} BTC invested".format(total))
print("{0:.3f} BTC grossed".format(money + sum([x['base'] for x in wallets])))
print("{0:.3f} BTC profit".format((money + sum([x['base'] for x in wallets])) - total))
print("start: {0}".format(candles[0]['data']['time'][0]))
print("end: {0}".format(candles[0]['data']['time'][-1]))
