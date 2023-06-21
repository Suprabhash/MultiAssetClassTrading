"""
Class to define an instrument
"""

class underlying:
    def __init__(self, underlying_ticker):
        self.underlying_ticker = underlying_ticker
        self.stock = None
        self.option_chain = None