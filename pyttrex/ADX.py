from pyttrex import  market_candles, market_summaries, ohlc_context
from talib.stream import ATR
import datetime
import pandas as pd
#https://www.forexfactory.com/showthread.php?t=285912
money = 0.1
total = money
markets = market_summaries(['BTC'], filtered=True)
wallets = [ {'name': m, 'last': 0, 'cost': 0, 'quantity': 0, 'price': 0, 'start': float(money / len(markets)), 'investing': float(money / len(markets))} for m in markets ]
candle = 'Day'
len_context = 12
len_context_short = 3
market_candles = market_candles(markets, candle)
backtest_list = zip(wallets, market_candles)

start, end = None, None
for coin in backtest_list:
    try:
        context = ohlc_context(len_context)
        context_short = ohlc_context(len_context_short)
        atrframes = ohlc_context(maxlen=None)
        positions = 0
        wallet = coin[0]
        if candle == 'Day':
            dataframes = coin[1]['data']
        else:
            dataframes = coin[1]['data'].resample('12H').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            })
    except:
        continue

    for row_time, row in dataframes.iterrows():
        atrframes['open'].append(row.open)
        atrframes['high'].append(row.high)
        atrframes['low'].append(row.low)
        atrframes['close'].append(row.close)
        atrframes['volume'].append(row.volume)
        atrframes['time'].append(row_time)
        atrframe = pd.DataFrame(atrframes)
        atrframe = atrframe.set_index(pd.to_datetime(atrframe['time']))
        atrargs = {'high': atrframe.close.values, 'low': atrframe.low.values, 'close': atrframe.close.values, 'timeperiod': 20 }

        #skip the rest to append the context untill it is full
        if len(context['open']) == len_context:
            exit_pos = min(context['low'])[0] if isinstance(min(context['low']), list) else min(context['low'])
            if row.high > max(context['high']) and positions <= 5 and wallet['investing'] > 0.001:
                positions+=1
                investment = wallet['investing'] - wallet['investing'] * 0.99 ** positions
                wallet['investing'] -= investment
                wallet['cost'] += investment
                wallet['quantity'] += ( investment / row.close ) - ( ( investment / row.close ) * 0.0025)
                wallet['price'] = 1 / (wallet['quantity'] / wallet['cost'])
                stop_loss = row.close - (2 * ATR(**atrargs))
                print(f"+{positions} {wallet['name']:7} {row_time} qty: {wallet['quantity']:5.2f} prc: {wallet['price']:11.8f} cls: {row.close:11.8f} sl {stop_loss:11.8f}")

            elif positions > 0:
                #stop loss
                if row.close <= stop_loss:
                    print(f"-{positions} {wallet['name']:7} {row_time} qty: {wallet['quantity']:5.2f} prc: {wallet['price']:11.8f} cls: {row.close:11.8f} sl {stop_loss:11.8f}")
                    wallet['investing'] += (wallet['quantity'] * row.close) - ((wallet['quantity'] * row.close) * 0.0025)
                    wallet['quantity'], wallet['cost'], positions = 0, 0, 0
                elif row.close <= exit_pos:
                    print(f"+-{positions} {wallet['name']:7} {row_time} qty: {wallet['quantity']:5.2f} prc: {wallet['price']:11.8f} cls: {row.close:11.8f} sl {stop_loss:11.8f}")
                    wallet['investing'] += (wallet['quantity'] * row.close) - ((wallet['quantity'] * row.close) * 0.0025)
                    wallet['quantity'], wallet['cost'], positions = 0, 0, 0

        context['open'].append(row.open)
        context['high'].append(row.high)
        context['low'].append(row.low)
        context['close'].append(row.close)
        context['volume'].append(row.volume)
        context['time'].append(row_time)
        context_short['open'].append(row.open)
        context_short['high'].append(row.high)
        context_short['low'].append(row.low)
        context_short['close'].append(row.close)
        context_short['volume'].append(row.volume)
        context_short['time'].append(row_time)

        start = row_time if not start else start
        end = row_time
        wallet['last'] = row.high


for test in sorted(wallets, key=lambda x: x['investing'], reverse=True):
    print({k: f'{v:.6f}' if isinstance(v, float) else v for k, v in test.items()})

for w in wallets:
    if w['quantity'] > 0:
        w['investing'] += w['last'] * w['quantity']
        w['quantity'] = 0

coin_money = sum([x['investing'] for x in wallets])
print("start: {0}".format(start))
print("end: {0}".format(end))
print("{0:+.3f} BTC starting capital".format(total))
if coin_money < total:
    print("{0:+.3f} BTC end total...sucker".format(coin_money))
elif coin_money > total:
    print("{0:+.3f} BTC end total shoop!".format(coin_money))
else:
    print("{0:+.3f} BTC end".format(coin_money))

for test in sorted(wallets, key=lambda x: x['investing'], reverse=True):
    print({k: f'{v:.6f}' if isinstance(v, float) else v for k, v in test.items()})
