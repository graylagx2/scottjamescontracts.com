# scottjamescontracts.com
A flask finance app to calculate strike prices for stock (call) options contracts. This app uses the python library yfinance to gather data on any stock ticker then combines the retrieved data with a contract term of the user choice to formulate a strike price for that options contract. All contract term available are actual available contracts on the market. f the contract term returns a strike price lower than the current price the user will be warned that the contract term should be lengthened or a (put) option should be considered.

![Screen shot of sofware image](https://github.com/graylagx2/Images/blob/master/home.png)![Screen shot of sofware image](https://github.com/graylagx2/Images/blob/master/contract_expiration.png)
![Screen shot of sofware image](https://github.com/graylagx2/Images/blob/master/contract_data.png)![Screen shot of sofware image](https://github.com/graylagx2/Images/blob/master/C_data_err.png)

**The formula used to calculate strike prices**

    (todays closing price) - (length of contract days ago) = strike

If the contract is 1 year in length or greater an 10% market correction is applied to the strike

    (strike) x (.9) = 10% correction strike price

# Make strike price calculations in python

def calculate_strike(self):
        # Make strike price calculations
        self.strike = round(
            (self.today_close - self.term_close) / 1.5 + self.today_close, 2
        )

        # Only apply 10% correction if contract is roughly 1 year
        # or greater. This could be adjusted to 16 months or 485 days
        if self.contract_days > 365:
            self.strike_shaved = round(self.strike * .90, 2)
        else:
            self.strike_shaved = None

        return self.strike, self.strike_shaved
