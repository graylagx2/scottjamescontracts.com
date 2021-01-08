#!/usr/bin/env python3

'''Python 3.6+

Title: Contracts.py

Version: Development/1.3

Author: Grant Getzfrid

Contributors: Scott James(Strike price formula)

Description:
    This file performs data fetching and price calculations for a flask
    server flask_server.py

PIP dependencies:
    numpy
	yfinance
	requests

Notes: N/A
'''

from datetime import date, datetime, timedelta
import numpy as np
import requests
import yfinance as yf


class ContractCalculator(object):

    def __init__(self, json, ticker):
        # Taking flasks import of json
        self.json = json

        # Taking flasks ticker from user input
        self.ticker = ticker

        # Formatting string to be uppercase because i think it looks
        # better on the web page
        if self.ticker.upper():
            self.ticker = self.ticker.upper()

        # Setting the ticker for yfinance
        self.stock = yf.Ticker(self.ticker)

        # Using Yahoo finance api to fetch tickers company name
        # This method is much faster and more reliable than yfinance
        # Yahoo finance api for ticker json data
        url = f"http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={self.ticker}&region=1&lang=en"

        # Fetching url data
        url_resp = requests.get(url)

        # Formating response in unicode
        url_json_unicode = url_resp.text

        # Loading json data
        json_data = self.json.loads(url_json_unicode)

        # Parsing the json data for tickers company name
        self.company = json_data['ResultSet']['Result'][0]['name']

    @property
    def ticker_details(self):
        # Retrieving tickers name and company name
        return self.ticker, self.company

    @property
    def get_option_contracts(self):
        # Turning every option contract date into a datetime object
        option_dates = [datetime.strptime(option_date, '%Y-%m-%d').date()
                        for option_date in self.stock.options
                        ]

        # If a date in the available option contracts is before
        # todays date we will remove it. This does happen sometimes because
        # yfinance is not always perfectly up to date.
        self.options = list(filter(
            lambda d: False if d < date.today() else True, option_dates
        ))

        return self.options

    def option_filter(self, expiration_string):
        # Converting the expiration date selected from a string to a date
        self.contract_date = datetime.strptime(
            expiration_string, "%Y-%m-%d"
        ).date()

        # Calculate how many days contract is
        self.current_date = date.today()
        self.contract_days = self.contract_date - self.current_date
        self.contract_days = self.contract_days.days
        # how ever many days the contract date this turns days ago into a date
        self.days_ago = self.current_date - timedelta(self.contract_days)

        # Filtering weekends out
        c_days = self.contract_days
        business_days = np.busday_count(self.days_ago, self.current_date)
        while business_days < self.contract_days:
            c_days += 1
            self.days_ago = self.current_date - timedelta(c_days)
            business_days = np.busday_count(self.days_ago, self.current_date)

        return self.contract_days

    @property
    def price_data(self):
        # Condition for same day contracts
        if self.contract_days < 1:
            # Download ticker data from today minus contract term in days
            self.stock_data = yf.download(self.ticker, self.current_date)

            # Because the contract is the same day we handle the table
            #  data differently then below. We need to grab same day
            # Open and close data
            self.term_close = self.stock_data.iloc[0, 0]  # Todays open
            self.today_close = self.stock_data.iloc[-1, -3]  # Todays close
            self.volatility = None

        else:
            # Download ticker data from today minus contract term in days
            self.stock_data = yf.download(
                self.ticker,
                start=self.days_ago,
                end=self.current_date + timedelta(1)
            )['Close']
            # Gather historical data according to the contract term.
            # Todays close and number of contract days in the past close
            #  from the data table
            self.term_close = self.stock_data.iloc[0]
            self.today_close = self.stock_data.iloc[-1]

        return self.today_close

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

    @property
    def calculate_volatility(self):
        # Because the contract term is more than one day we can
        # calculate volatility
        # Number of data points
        total_data_points = len(self.stock_data)

        # Getting the sum of all past days close price
        sum_days_close = round(self.stock_data.sum(), 2)

        # Getting the mean of all close prices
        mean = sum_days_close / total_data_points

        # Iterating over datapoints and subtracting the mean from each data
        #  point
        deviations = list(map(
            lambda i: i - mean, self.stock_data
        ))

        # Iterating over deviations and squaring each deviation
        squared_deviations = list(map(
            lambda deviation: deviation ** 2, deviations
        ))

        # Adding all the squares together
        squares_sum = sum(squared_deviations)

        # Find the mean of the squared deviations
        squares_mean = round(squares_sum / total_data_points, 2)

        # Final step in getting volatility is to square root the mean
        # of the squares_mean
        self.volatility = round(squares_mean**(.5), 2)

        return self.volatility

    @property
    def get_holders(self):
        # finding the index type of the dataframe because standard stocks
        # have type O strings and trusts have int64
        # This is only different on the institutional holders dataframe
        ih_type = self.stock.institutional_holders.columns.dtype

        # If the institutional holders data frame is int64
        # This of for trusts only
        if ih_type == "int64":
            # Creating institutional holders table data
            ih_trust_df = self.stock.institutional_holders

            # Turning institutional holders dataframe into json
            ih_trust_df_json = ih_trust_df.to_json(orient='index')
            self.ih_trust_table_json = self.json.loads(ih_trust_df_json)

            # Creating major holders table data
            mh_trust_df = self.stock.major_holders

            # Turning major holders dataframe into json
            mh_trust_df_json = mh_trust_df.to_json(orient='index')
            self.mh_trust_table_json = self.json.loads(mh_trust_df_json)

            # We have to set the standard stocks to none for the flask server
            # can still return them with out error
            self.ih_table_json = None
            self.mh_table_json = None

            return (
                self.mh_table_json,
                self.ih_table_json,
                self.mh_trust_table_json,
                self.ih_trust_table_json
            )

        else:
            # Creating the institutional holders table a excluding the date
            ih_df = self.stock.institutional_holders.drop(
                ['Date Reported'], axis=1)

            # Turning institutional holders dataframe into json
            ih_df_json = ih_df.to_json(orient='index')
            self.ih_table_json = self.json.loads(ih_df_json)

            # Creating table data to export to html
            mh_df = self.stock.major_holders

            # Turning major holders dataframe into json
            mh_df_json = mh_df.to_json(orient='index')
            self.mh_table_json = self.json.loads(mh_df_json)

            # Setting trust table to none so flask server doesn't throw error
            self.ih_trust_table_json = None
            self.mh_trust_table_json = None

            return (
                self.mh_table_json,
                self.ih_table_json,
                self.mh_trust_table_json,
                self.ih_trust_table_json
            )
