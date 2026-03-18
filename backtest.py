import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class BacktestingEngine:
    """Backtesting engine to test signal accuracy on historical data"""
    
    def __init__(self):
        self.trades = []
        self.signals = []
        self.accuracy_results = {}
    
    def generate_sample_data(self, symbol, days=100):
        """Generate sample historical data"""
        np.random.seed(42)
        dates = pd.date_range(end=datetime.now(), periods=days, freq='1D')
        
        if symbol == 'BTC':
            start_price = 45000
        else:  # GOLD
            start_price = 2000
        
        prices = [start_price]
        for i in range(1, days):
            change = np.random.normal(0, 2)
            prices.append(prices[-1] * (1 + change/100))
        
        df = pd.DataFrame({
            'timestamp': dates,
            'open': prices,
            'high': [p * 1.02 for p in prices],
            'low': [p * 0.98 for p in prices],
            'close': prices,
            'volume': np.random.randint(1000, 10000, days)
        })
        
        return df
    
    def calculate_rsi(self, data, period=14):
        """Calculate RSI indicator"""
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, data):
        """Calculate MACD indicator"""
        exp1 = data['close'].ewm(span=12, adjust=False).mean()
        exp2 = data['close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=9, adjust=False).mean()
        return macd, signal_line
    
    def generate_signals(self, data):
        """Generate buy/sell signals"""
        data = data.copy()
        data['rsi'] = self.calculate_rsi(data)
        data['macd'], data['signal_line'] = self.calculate_macd(data)
        
        signals = []
        for i in range(len(data)):
            if i < 26:
                signals.append('HOLD')
            else:
                rsi = data['rsi'].iloc[i]
                macd = data['macd'].iloc[i]
                signal_line = data['signal_line'].iloc[i]
                
                if rsi < 30 and macd < signal_line:
                    signals.append('BUY')
                elif rsi > 70 and macd > signal_line:
                    signals.append('SELL')
                else:
                    signals.append('HOLD')
        
        data['signal'] = signals
        return data
    
    def backtest(self, symbol, data):
        """Run backtest on historical data"""
        data_with_signals = self.generate_signals(data)
        
        trades = []
        portfolio_value = 10000
        position = None
        entry_price = 0
        
        for i in range(len(data_with_signals)):
            current_price = data_with_signals['close'].iloc[i]
            signal = data_with_signals['signal'].iloc[i]
            
            if signal == 'BUY' and position is None:
                position = 'LONG'
                entry_price = current_price
                trades.append({
                    'symbol': symbol,
                    'action': 'BUY',
                    'price': current_price,
                    'date': data_with_signals['timestamp'].iloc[i]
                })
            
            elif signal == 'SELL' and position == 'LONG':
                exit_price = current_price
                profit_percent = ((exit_price - entry_price) / entry_price) * 100
                portfolio_value *= (1 + profit_percent/100)
                
                trades.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'price': exit_price,
                    'profit_percent': profit_percent,
                    'date': data_with_signals['timestamp'].iloc[i]
                })
                position = None
        
        return trades, portfolio_value, data_with_signals
    
    def calculate_accuracy(self, trades):
        """Calculate trading accuracy"""
        if len(trades) < 2:
            return 0
        
        profitable_trades = 0
        total_trades = 0
        
        for i in range(0, len(trades)-1, 2):
            if i+1 < len(trades):
                total_trades += 1
                if trades[i+1].get('profit_percent', 0) > 0:
                    profitable_trades += 1
        
        accuracy = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
        return accuracy
    
    def run_backtest(self):
        """Run complete backtest for both symbols"""
        symbols = ['BTC', 'GOLD']
        results = {}
        
        print("="*80)
        print("CRYPTO-FOREX TRADING BOT - BACKTESTING RESULTS")
        print("="*80)
        print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()        
        for symbol in symbols:
            print(f"\n{'='*80}")
            print(f"BACKTESTING: {symbol}")
            print(f"{'='*80}")
            
            # Generate historical data
            data = self.generate_sample_data(symbol, days=100)
            
            # Run backtest
            trades, final_portfolio, signals_data = self.backtest(symbol, data)
            
            # Calculate accuracy
            accuracy = self.calculate_accuracy(trades)
            
            # Store results
            results[symbol] = {
                'trades': trades,
                'accuracy': accuracy,
                'portfolio_value': final_portfolio,
                'total_trades': len(trades),
                'buy_signals': len([t for t in trades if t['action'] == 'BUY']),
                'sell_signals': len([t for t in trades if t['action'] == 'SELL'])
            }
            
            # Print results
            print(f"\n📊 BACKTESTING RESULTS FOR {symbol}:")
            print(f"{'─'*80}")
            print(f"Total Trades: {len(trades)}")
            print(f"Buy Signals: {results[symbol]['buy_signals']}")
            print(f"Sell Signals: {results[symbol]['sell_signals']}")
            print(f"Signal Accuracy: {accuracy:.2f}%")
            print(f"Final Portfolio Value: ${final_portfolio:,.2f}")
            print(f"Return: {((final_portfolio - 10000) / 10000 * 100):.2f}%")
            print(f"{'─'*80}")
            
            if len(trades) > 0:
                print(f"\n📈 RECENT TRADES:")
                for trade in trades[-5:]:
                    print(f"  {trade['action']:5} | {trade['date'].strftime('%Y-%m-%d')} | ${trade['price']:,.2f}", end="")
                    if 'profit_percent' in trade:
                        print(f" | Profit: {trade['profit_percent']:+.2f}%")
                    else:
                        print()
        
        print(f"\n{'='*80}")
        print("OVERALL SUMMARY")
        print(f"{'='*80}")
        
        btc_accuracy = results['BTC']['accuracy']
        gold_accuracy = results['GOLD']['accuracy']
        avg_accuracy = (btc_accuracy + gold_accuracy) / 2
        
        print(f"Bitcoin Accuracy: {btc_accuracy:.2f}%")
        print(f"Gold Accuracy: {gold_accuracy:.2f}%")
        print(f"Average Accuracy: {avg_accuracy:.2f}%")
        print(f"\n✅ Status: {'READY FOR LIVE TRADING' if avg_accuracy > 60 else 'NEEDS OPTIMIZATION'}")
        print(f"{'='*80}\n")
        
        return results

if __name__ == '__main__':
    engine = BacktestingEngine()
    results = engine.run_backtest()