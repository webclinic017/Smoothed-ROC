##### ----- Based on Peter Nistrup's Medium Article ----- #####

# IMPORTS
import pandas as pd
import math
import os.path
from binance.client import Client
from datetime import datetime
import time
from dateutil import parser
import keys
from pathlib import Path
import extensions as ex

### CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
batch_size = 750
binance_client = Client(api_key=keys.Pkey, api_secret=keys.Skey)


### FUNCTIONS
def minutes_of_new_data(symbol, kline_size, data, source):
    if len(data) > 0:
        old = parser.parse(data["timestamp"].iloc[-1])
    elif source == "binance":
        old = datetime.strptime('1 Jan 2017', '%d %b %Y')
    if source == "binance":
        new = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    return old, new


def get_all_binance(symbol, kline_size, save = False):
    filename = Path(f'Z:/Data/{symbol}-{kline_size}-data.csv')
    if os.path.isfile(filename):
        data_df = pd.read_csv(filename)
    else:
        print('no file found')
        data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source="binance")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'):
        print(f'Downloading all available {kline_size} data for {symbol}, {int(delta_min)} minutes of data. Be patient..!')
    else:
        print(f'Downloading {delta_min} minutes of new data available for {symbol}, i.e. {available_data} instances of {kline_size} data.')
    klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else: data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save:
        data_df.to_csv(filename, date_format='%Y-%m-%d %H:%M:%S')
    print('All caught up..!')
    return data_df


### RUN

start = time.perf_counter()

if os.path.isdir(Path('Z:/Data')):
    pairs = ex.get_pairs('USDT')
    print('pairs list: ', pairs)
    for i in range(len(pairs)):
        get_all_binance(pairs[i], '1m', save=True)
        print(f'{i+1} of {len(pairs)} done!')

    # get_all_binance('BTCUSDT', '1m', save=True)

    end = time.perf_counter()
    total = round(end - start)
    print(f'Time taken: {total//60}m {total%60}s')
else:
    print('Data folder not found, fix connection and try again')