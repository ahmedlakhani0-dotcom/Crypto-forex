import numpy as np
import pandas as pd
import talib

class SignalGenerator:
    def __init__(self, data):
        self.data = data

    def calculate_indicators(self):
        self.data['RSI'] = talib.RSI(self.data['Close'], timeperiod=14)
        self.data['MACD'], self.data['MACD_signal'], _ = talib.MACD(self.data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        self.data['Upper_BB'], self.data['Lower_BB'] = talib.BBANDS(self.data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)[0:2]

    def generate_signals(self):
        signals = []
        confidence_levels = []

        for i in range(len(self.data)):
            if self.data['RSI'][i] < 30 and self.data['Close'][i] < self.data['Lower_BB'][i]:
                signals.append('Buy')
                confidence_levels.append('High')
            elif self.data['RSI'][i] > 70 and self.data['Close'][i] > self.data['Upper_BB'][i]:
                signals.append('Sell')
                confidence_levels.append('High')
            else:
                signals.append('Hold')
                confidence_levels.append('Low')

        self.data['Signal'] = signals
        self.data['Confidence'] = confidence_levels

    def get_signals(self):
        self.calculate_indicators()
        self.generate_signals()
        return self.data[['Close', 'Signal', 'Confidence']]

# Example usage:
# data = pd.DataFrame({'Close': [...]})
# generator = SignalGenerator(data)
# signals = generator.get_signals()