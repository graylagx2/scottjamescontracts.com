'''Python 3.6+

Title: Contracts.py

Version: Production 1.1

Author: Grant Getzfrid

Contributors: N/A

Description:
    Flask app that generates a strike price for stock option contracts using 
    contract_calculator.py. The user is first prompted to input a stock ticker 
    then to pick the expiration date of the contract. That data is then used 
    to fetch historical price data specific to the contract term and calculate 
    a strike price.

Dependencies:
    contract_calculator.py

PIP dependencies:
	flask

Notes:

'''
from contract_calculator import ContractCalculator
from flask import (
    Flask,
    request,
    json,
    jsonify,
    render_template,
    redirect,
    url_for,
    session
)
from flask_mail import Message, Mail
import os

# Instantiating the flask object
app = Flask(__name__)

# Using the production configuration
app.config.from_object('config.ProdConfig')

# Instantiating the mail object
mail = Mail(app)


# View function for the root directory / home page
@app.route("/", methods=['GET', 'POST'])
def home():
    # Handling POST requests
    if request.method == 'POST':
        if 'contact-us' in request.form:
            return_email = request.form['return-email']
            email_subject = request.form['subject']
            email_body = request.form['message-body']
            msg = Message(
                subject=email_subject,
                sender=app.config.get("MAIL_USERNAME"),
                recipients=["scottjamescontracts@gmail.com"],
                body=f"{return_email} says:\n{email_body}"
            )
            mail.send(msg)

            return redirect(url_for('home'))

        if 'ticker_input' in request.form:

            # Getting input from html form data from the html name attribute
            ticker = request.form["ticker_input"]

            # Creating a cookie session to pass data to other view functions
            session['ticker'] = ticker

            # Sending user to next page to fill in contract expiration date
            # and sending variables to that view function by URL arguments.
            return redirect(url_for('contractexpiration'))

    if request.method == 'GET':
        # Handling invalid input from user when redirected back home for invalid
        #  ticker input or no contracts available for ticker
        # The url will contain which error was raised
        if request.args.get('error') == "Invalid-ticker":
            return render_template(
                'home.html',
                invalid_ticker="Invalid ticker: Please enter a valid ticker"
            )

        elif request.args.get('error') == "No-options-available":
            return render_template(
                'home.html',
                invalid_ticker="Not available: Could not find options for ticker"
            )

        # Restting the session for home page get
        #  Return home.html if the request is a get request
        return render_template('home.html')


# View function for the contract expiration select page
@app.route("/contractexpiration", methods=['GET', 'POST'])
def contractexpiration():
    # Technically someone could go to scottjames.com/contractexpiration with
    # out ever inputting a ticker from the homepage by simply typing in that
    # specific url so we will be sure we have a session before continuing
    # else wi will redirect them back home
    if 'ticker' in session:
        # Getting the ticker sent from home page session
        ticker = session.get('ticker')
        try:
            # Instantiating out contractcalculator class from
            # contract_calculator.py
            # Sending flasks json over to contract_calculator to avoid extra
            #  imports
            generate = ContractCalculator(json, ticker)

            # Assigning the ticker and company variable from tuple returned
            # from ticker_details function in contract_calculator.py
            ticker, company = generate.ticker_details

            # Fetching available option contracts from get_option_contracts
            # function in contract_calculator.py
            options = generate.get_option_contracts

            # Raise exception if there are zero options because ticker does not
            #  have options contracts available
            if len(options) == 0:
                raise ValueError()

        # Redirect home if ticker was invalid
        except IndexError:
            return redirect(url_for('home', error="Invalid-ticker"))
        # Redirect home if ticker had no options available
        except ValueError:
            return redirect(url_for('home', error="No-options-available"))

        # If everything everthing was good we can continue to allow a POST
        #  request
        else:
            # Handling POST requests only
            if request.method == 'POST':
                # Get the contract expiration date from select tags name attrib
                expiration_string = request.form["form_select"]

                contract_days = generate.option_filter(expiration_string)

                todays_close = generate.price_data

                strike_prices = generate.calculate_strike()

                if contract_days > 0:
                    volatility = generate.calculate_volatility
                else:
                    volatility = None

                holders = generate.get_holders

                # Creating a dictionary to avoid a messy return
                data = {
                    'ticker': ticker,
                    'company': company,
                    'options': options,
                    'current_price': round(todays_close, 2),
                    'term': contract_days,
                    'strike': strike_prices[0],
                    'strike_shaved': strike_prices[1],
                    'volatility': volatility,
                    'mh_table_data': holders[0],
                    'ih_table_data': holders[1],
                    'mh_trust_table_data': holders[2],
                    'ih_trust_table_data': holders[3]
                }

                return render_template('contractdata.html', **data)

    # Redirecting user home if the typed scottjames.com/contractexpiration
    # straight into browser url bar
    else:
        return redirect(url_for('home'))

    return render_template(
        'contractexpiration.html',
        ticker=ticker,
        company=company,
        options=options
    )


# Routing our manifest.json for PWA capability
@app.route('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')


# A control to insure the app is only ran if this file is called directly
# rather than importe
if __name__ == "__main__":
    app.run()
