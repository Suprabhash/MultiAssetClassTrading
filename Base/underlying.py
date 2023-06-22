"""
Class to define an instrument
"""
import pandas as pd
from kiteconnect import KiteConnect
from credentials.kite import access_token, api_key
import datetime

from Base.call import call
from Base.put import put

class underlying:
    def __init__(self, underlying_ticker):
        self.underlying_ticker = underlying_ticker
        self.stock = None
        self.options = {}
        self.futures = None

    def get_option_matrix(self):
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)

        ticker_name = self.underlying_ticker
        nso = kite.instruments('NFO')
        nso_data = pd.DataFrame(nso)
        self.options_matrix = nso_data[(nso_data.name == ticker_name) & (nso_data.segment == 'NFO-OPT')].set_index(["expiry", "strike", "instrument_type"])[["instrument_token"]] 


    def create_options_contracts(self):
        self.option_expiries = list(set(self.get_expiry_list(self.options_matrix)))
        self.options = {}
        for expiry in self.option_expiries:
            self.options[expiry] = {}
            option_strikes = self.get_strike_list(self.options_matrix, expiry)
            for strike in option_strikes:
                self.options[expiry][strike] = {}
                self.options[expiry][strike]["call"] = call(self, expiry, strike, 
                                                            self.get_option_token(self.options_matrix, expiry, strike, "CE"))
                self.options[expiry][strike]["put"] = put(self, expiry, strike,
                                                          self.get_option_token(self.options_matrix, expiry, strike, "PE"))
        
    def get_data_for_all_options_contracts(self, start_date, end_date, interval):
        for expiry in self.option_expiries:
            option_strikes = self.get_strike_list(self.options_matrix, expiry)
            for strike in option_strikes:
                self.options[expiry][strike]["call"].get_data(start_date, end_date, interval)
                self.options[expiry][strike]["put"].get_data(start_date, end_date, interval)
        

    @staticmethod
    def get_expiry_list(options_matrix):
        return list(options_matrix.index.get_level_values('expiry'))

    @staticmethod
    def get_strike_list(options_matrix, expiry):
        strikes = list(set(options_matrix.iloc[(options_matrix.index.get_level_values('expiry') == expiry)]
                           .index.get_level_values('strike')))
        strikes.sort()
        return strikes
    
    @staticmethod
    def get_option_token(options_matrix, expiry, strike, instrument_type):
        return options_matrix.iloc[(options_matrix.index.get_level_values('expiry') == expiry)&
                                   (options_matrix.index.get_level_values('strike') == strike)&
                                   (options_matrix.index.get_level_values('instrument_type') == instrument_type)]["instrument_token"].iloc[0]