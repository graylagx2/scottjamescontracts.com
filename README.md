# scottjamescontracts.com
A flask finance app to calculate strike prices for stock (call) options contracts. This app uses the python library yfinance to gather data on any stock ticker then combines the retrieved data with a contract term of the user choice to formulate a strike price for that options contract. All contract term available are actual available contracts on the market. f the contract term returns a strike price lower than the current price the user will be warned that the contract term should be lengthened or a (put) option should be considered.

![Screen shot of sofware image](https://github.com/graylagx2/Images/blob/master/home.png)![Screen shot of sofware image](https://github.com/graylagx2/Images/blob/master/contract_expiration.png)
![Screen shot of sofware image](https://github.com/graylagx2/Images/blob/master/contract_data.png)![Screen shot of sofware image](https://github.com/graylagx2/Images/blob/master/c_data_err.png)
