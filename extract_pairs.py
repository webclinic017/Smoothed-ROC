import pandas as pd

screener_data = pd.read_csv('crypto_2019-12-10.csv')

print(screener_data.head())

pairs = list(screener_data['Ticker'])

symbols = pairs[:10]

print('pairs list: ', symbols)