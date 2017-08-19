from pyttrex import ohlc, market_summaries
from talib.stream import ATR

from queue import Queue
from threading import Thread

def table_results(atrdata):
    url='https://bittrex.com/Market/Index?MarketName='
    head = "| {0} | {1} | {2} | {3} | {4} |".format("PAIR".ljust(9),
                                                    "short".ljust(8),
                                                    "medium".ljust(8),
                                                    "long".ljust(8),
                                                    "URL".ljust(len(url)+9))
    horizontal_line = len(head) * "-"
    table=horizontal_line+'\n'+head+'\n'+horizontal_line+'\n'
    for c in atrdata:
        short, medium, long = round(c['short'], 4), round(c['medium'], 4), round(c['long'], 4)
        row = [c['name'].ljust(9), str(short).ljust(8), str(medium).ljust(8), str(long).ljust(8), str(url+c['name']).ljust(len(url) + 9)] if short > medium > long else None
        table+="| {0} | {1} | {2} | {3} | {4} |\n".format(*row) if row is not None else ""
    table+=horizontal_line
    return table

inputs = {}
def worker():
    while True:
        item = q.get()
        result = ohlc(item, 'OneMin')
        try:
            inputs[result['name']] = result['candles'] if result['candles'] else False
        except:
            print("cant talk to trex for coin {0}".format(item))
        finally:
            q.task_done()

q = Queue()
for i in range(4):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in market_summaries(['BTC', 'ETH']):
    q.put(item)
q.join()

if __name__ == '__main__':
    output = []
    for c in inputs:
        try:
            kwargs = {'high': inputs[c]['H'], 'low': inputs[c]['L'], 'close': inputs[c]['C']}
            output.append({'name': c,
                           'short': ATR(**kwargs, timeperiod=9),
                           'medium': ATR(**kwargs, timeperiod=27),
                           'long': ATR(**kwargs, timeperiod=81)})
        except:
            pass

    data = sorted(output, key=lambda x: x['short'], reverse=True)
    print(table_results(data))