"""

"""
from kiteconnect import KiteConnect
import pandas as pd
import datetime

from credentials.kite import access_token, api_key

class future:
    def __init__(self, underlying, expiry, token):
        self.underlying = underlying
        self.underlying_ticker = underlying.underlying_ticker
        self.expiry = expiry
        self.token = token

    def get_data(self, start_date, end_date, interval):
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)

        kite_data_historical = kite.historical_data(self.token, start_date, end_date, interval, continuous=False, oi=True)
        self.data = pd.DataFrame(kite_data_historical)


    
