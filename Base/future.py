"""

"""
from kiteconnect import KiteConnect
import pandas as pd
import datetime

from credentials.kite import access_token, api_key

class future:
    def __init__(self, underlying):
        self_underlying = underlying
        self.underlying_ticker = underlying.underlying_ticker
        underlying.future = self

    def get_data(self, start_date, end_date, interval):
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)

        ticker_name = self.underlying_ticker
        nse_data = pd.DataFrame(kite.instruments('NSE'))

        token = nse_data[nse_data.tradingsymbol == ticker_name].instrument_token.values[0]
        kite_data_historical = kite.historical_data(token, start_date,
                                                    end_date,
                                                    interval, continuous=False, oi=False)
        self.data = pd.DataFrame(kite_data_historical)
