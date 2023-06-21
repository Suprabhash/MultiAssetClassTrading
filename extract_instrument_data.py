#!python
import datetime
import logging
from kiteconnect import KiteConnect
import pprint
import pandas as pd
import plotly.graph_objects as go

logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key="i1kdmhmd191859jo")

access_token = '6Ky8H1ghUnZoKAzK7TeE5Fc5cBKULYi9'
kite.set_access_token(access_token)

ticker_name = 'HDFC'

nse = kite.instruments('NSE')
nse_data = pd.DataFrame(nse)

# print(nse_data[nse_data.tradingsymbol.str.contains('HDFC')])

nse_data[nse_data.tradingsymbol.str.contains('HDFC')].to_csv('test.csv')
format = "%Y-%m-%d %H:%M:%S"

token = nse_data[nse_data.tradingsymbol == ticker_name].instrument_token.values[0]
kite_data_historical = kite.historical_data(token, "2021-01-01 00:01:00",
                                            datetime.datetime.now().strftime(format),
                                            'day', continuous=False, oi=True)
rcom_be = pd.DataFrame(kite_data_historical)
rcom_be.to_csv(ticker_name + '_data.csv')
df = rcom_be

fig = go.Figure(data=[go.Candlestick(x=df['date'],
                                     open=df['open'], high=df['high'],
                                     low=df['low'], close=df['close'])
                      ])

fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()

nso = kite.instruments('NFO')
nso_data = pd.DataFrame(nso)

futures_tokens = nso_data[(nso_data.name == ticker_name) & (nso_data.segment == 'NFO-FUT')].instrument_token
print(futures_tokens)

for futures_token in futures_tokens:
    kite_data_historical = kite.historical_data(futures_token, "2021-01-01 00:01:00",
                                                datetime.datetime.now().strftime(format),
                                                'day', continuous=False, oi=True)
    kite_data_historical_df = pd.DataFrame(kite_data_historical).to_csv('futures'+str(futures_token)+'.csv')


options_tokens = nso_data[(nso_data.name == ticker_name) & (nso_data.segment == 'NFO-OPT')].instrument_token
print(options_tokens)

for options_token in options_tokens:
    kite_data_historical = kite.historical_data(options_token, "2021-01-01 00:01:00",
                                                datetime.datetime.now().strftime(format),
                                                'day', continuous=False, oi=True)
    kite_data_historical_df = pd.DataFrame(kite_data_historical).to_csv('options'+str(options_token)+'.csv')









