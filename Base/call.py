from Base.option import option

class call(option):
    def __init__(self, underlying, expiry, strike, token):
        option.__init__(self, underlying, expiry, strike, token)
        self.option_type = "call"