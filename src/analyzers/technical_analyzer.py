import pandas as pd
import numpy as np
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    def __init__(self, short_ma=[5, 10], mid_ma=[20, 40], long_ma=[60, 120]):
        self.short_ma = short_ma
        self.mid_ma = mid_ma
        self.long_ma = long_ma

    def calculate_ma(self, df: pd.DataFrame, periods: List[int]) -> pd.DataFrame:
        for period in periods:
            df[f'MA{period}'] = df['Close'].rolling(window=period).mean()
        
        df['MA_Short'] = df['Close'].rolling(window=self.short_ma[0]).mean()
        df['MA_Mid'] = df['Close'].rolling(window=self.mid_ma[0]).mean()
        df['MA_Long'] = df['Close'].rolling(window=self.long_ma[0]).mean()
        
        return df

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df

    def calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        exp1 = df['Close'].ewm(span=fast, adjust=False).mean()
        exp2 = df['Close'].ewm(span=slow, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_SIGNAL'] = df['MACD'].ewm(span=signal, adjust=False).mean()
        df['MACD_HIST'] = df['MACD'] - df['MACD_SIGNAL']
        return df

    def calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20, std_dev: int = 2) -> pd.DataFrame:
        df['BB_MIDDLE'] = df['Close'].rolling(window=period).mean()
        df['BB_UPPER'] = df['BB_MIDDLE'] + (df['Close'].rolling(window=period).std() * std_dev)
        df['BB_LOWER'] = df['BB_MIDDLE'] - (df['Close'].rolling(window=period).std() * std_dev)
        return df

    def analyze_trend(self, df: pd.DataFrame) -> Dict:
        try:
            latest = df.iloc[-1]
            analysis = {'trend': '中性', 'strength': '弱'}
            
            if 'MA5' in df.columns and 'MA20' in df.columns:
                if latest['MA5'] > latest['MA20']:
                    analysis['trend'] = '上升'
                    analysis['strength'] = '强' if latest['MA5'] > df['MA5'].iloc[-2] else '中'
                else:
                    analysis['trend'] = '下降'
                    analysis['strength'] = '强' if latest['MA5'] < df['MA5'].iloc[-2] else '中'
            
            return analysis
        except Exception as e:
            logger.error(f"趋势分析失败: {e}")
            return {'trend': '未知', 'strength': '未知'}

    def analyze_support_resistance(self, df: pd.DataFrame) -> Dict:
        try:
            recent_highs = df['High'].tail(20).max()
            recent_lows = df['Low'].tail(20).min()
            current_price = df['Close'].iloc[-1]
            
            return {
                'resistance': recent_highs,
                'support': recent_lows,
                'current_price': current_price,
                'position': '偏高' if current_price > (recent_highs + recent_lows) / 2 else '偏低'
            }
        except Exception as e:
            logger.error(f"支撑阻力分析失败: {e}")
            return {}

    def generate_signals(self, df: pd.DataFrame) -> Dict:
        try:
            latest = df.iloc[-1]
            signals = {
                'buy_signals': [],
                'sell_signals': [],
                'overall_signal': '持有'
            }
            
            if 'RSI' in df.columns:
                if latest['RSI'] < 30:
                    signals['buy_signals'].append('RSI超卖')
                elif latest['RSI'] > 70:
                    signals['sell_signals'].append('RSI超买')
            
            if 'MACD_HIST' in df.columns and len(df) > 1:
                if latest['MACD_HIST'] > 0 and df['MACD_HIST'].iloc[-2] <= 0:
                    signals['buy_signals'].append('MACD金叉')
                elif latest['MACD_HIST'] < 0 and df['MACD_HIST'].iloc[-2] >= 0:
                    signals['sell_signals'].append('MACD死叉')
            
            if 'BB_LOWER' in df.columns and 'BB_UPPER' in df.columns:
                if latest['Close'] < latest['BB_LOWER']:
                    signals['buy_signals'].append('价格跌破下轨')
                elif latest['Close'] > latest['BB_UPPER']:
                    signals['sell_signals'].append('价格突破上轨')
            
            buy_score = len(signals['buy_signals'])
            sell_score = len(signals['sell_signals'])
            
            if buy_score > sell_score:
                signals['overall_signal'] = '买入'
            elif sell_score > buy_score:
                signals['overall_signal'] = '卖出'
            
            return signals
        except Exception as e:
            logger.error(f"信号生成失败: {e}")
            return {}

    def analyze(self, df: pd.DataFrame) -> Dict:
        try:
            if df.empty or len(df) < 60:
                return {}
            
            df = self.calculate_ma(df, self.short_ma + self.long_ma)
            df = self.calculate_rsi(df)
            df = self.calculate_macd(df)
            df = self.calculate_bollinger_bands(df)
            
            trend = self.analyze_trend(df)
            support_resistance = self.analyze_support_resistance(df)
            signals = self.generate_signals(df)
            
            return {
                'trend': trend,
                'support_resistance': support_resistance,
                'signals': signals,
                'current_data': {
                    'price': df['Close'].iloc[-1],
                    'ma5': df['MA5'].iloc[-1] if 'MA5' in df.columns else None,
                    'ma20': df['MA20'].iloc[-1] if 'MA20' in df.columns else None,
                    'rsi': df['RSI'].iloc[-1] if 'RSI' in df.columns else None,
                    'macd': df['MACD'].iloc[-1] if 'MACD' in df.columns else None
                }
            }
        except Exception as e:
            logger.error(f"技术分析失败: {e}")
            return {}
