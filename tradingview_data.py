import yfinance as yf

class TradingViewData:
    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_ohlcv(self):
        data = yf.Ticker(self.ticker).history(period='1d')
        return data[['Open', 'High', 'Low', 'Close', 'Volume']]

    def fetch_current_price(self):
        data = yf.Ticker(self.ticker)
        return data.history(period='1d')['Close'][-1]

if __name__ == '__main__':
    btc_data = TradingViewData('BTC-USD')
    gold_data = TradingViewData('GC=F')

    print('Bitcoin OHLCV Data:')
    print(btc_data.fetch_ohlcv())
    print('Current Bitcoin Price:', btc_data.fetch_current_price())

    print('\nGold OHLCV Data:')
    print(gold_data.fetch_ohlcv())
    print('Current Gold Price:', gold_data.fetch_current_price())