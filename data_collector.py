import requests
import pandas as pd

class DataCollector:
    def __init__(self, base_url, symbol):
        self.base_url = base_url
        self.symbol = symbol

    def get_historical_data(self, interval, start_time, end_time):
        url = f'{self.base_url}/data/v2/kline'
        params = {
            'symbol': self.symbol,
            'interval': interval,
            'startTime': start_time,
            'endTime': end_time
        }
        response = requests.get(url, params=params)
        return response.json()

    def get_real_time_data(self):
        url = f'{self.base_url}/data/v2/last_kline'
        params = {'symbol': self.symbol}
        response = requests.get(url, params=params)
        return response.json()

if __name__ == '__main__':
    # Replace with your required values
    base_url = 'https://www.mexc.com'
    symbols = ['BTC_USDT', 'GOLD_USDT']
    data_collectors = {symbol: DataCollector(base_url, symbol) for symbol in symbols}

    # Example Usage:
    for symbol, collector in data_collectors.items():
        print(f'Collecting data for {symbol}...')
        historical_data = collector.get_historical_data('1d', '1609459200000', '1612137600000')  # Example timestamps
        print(historical_data)