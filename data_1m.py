import keys
import datetime
from binance.client import Client
import pandas as pd

client = Client(keys.Pkey, keys.Skey)
symbol = 'BTCUSDT'
klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "1 Jan, 2017")

BTC = pd.DataFrame(klines, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
BTC['Open Time'] = pd.to_datetime(BTC['Open Time'], unit='ms')
BTC.set_index('Open Time', inplace=True)

BTC.to_csv('BTC_1m_'+str(datetime.datetime.now().strftime("%Y_%m_%d")) + '.csv', date_format='%Y-%m-%d %H:%M:%S')
