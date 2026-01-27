import pandas as pd
import numpy as np
import logging
from typing import Dict, List
import talib
from scipy import stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedTechnicalAnalyzer:
    def __init__(self):
        self.short_ma = [5, 10]
        self.mid_ma = [20, 40]
        self.long_ma = [60, 120]

    def calculate_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA10'] = df['Close'].rolling(window=10).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA40'] = df['Close'].rolling(window=40).mean()
        df['MA60'] = df['Close'].rolling(window=60).mean()
        df['MA120'] = df['Close'].rolling(window=120).mean()
        
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        
        return df

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df

    def calculate_stochastic(self, df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
        low_min = df['Low'].rolling(window=k_period).min()
        high_max = df['High'].rolling(window=k_period).max()
        
        df['%K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
        df['%D'] = df['%K'].rolling(window=d_period).mean()
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
        df['BB_WIDTH'] = (df['BB_UPPER'] - df['BB_LOWER']) / df['BB_MIDDLE']
        df['BB_PERCENT'] = (df['Close'] - df['BB_LOWER']) / (df['BB_UPPER'] - df['BB_LOWER'])
        return df

    def calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        high = df['High']
        low = df['Low']
        close = df['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        df['ATR'] = tr.rolling(window=period).mean()
        return df

    def calculate_cci(self, df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
        tp = (df['High'] + df['Low'] + df['Close']) / 3
        sma_tp = tp.rolling(window=period).mean()
        mad = tp.rolling(window=period).apply(lambda x: np.abs(x - x.mean()).mean())
        df['CCI'] = (tp - sma_tp) / (0.015 * mad)
        return df

    def calculate_williams_r(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        high_max = df['High'].rolling(window=period).max()
        low_min = df['Low'].rolling(window=period).min()
        df['Williams_R'] = -100 * ((high_max - df['Close']) / (high_max - low_min))
        return df

    def calculate_volume_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
        df['Volume_MA20'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_MA20']
        
        price_change = df['Close'].pct_change()
        volume_change = df['Volume'].pct_change()
        df['VWAP'] = (df['Close'] * df['Volume']).rolling(window=20).sum() / df['Volume'].rolling(window=20).sum()
        
        return df

    def calculate_momentum(self, df: pd.DataFrame, period: int = 10) -> pd.DataFrame:
        df['Momentum'] = df['Close'] - df['Close'].shift(period)
        df['ROC'] = ((df['Close'] - df['Close'].shift(period)) / df['Close'].shift(period)) * 100
        return df

    def calculate_fibonacci_retracement(self, df: pd.DataFrame, lookback: int = 100) -> Dict:
        recent_df = df.tail(lookback)
        high_point = recent_df['High'].max()
        low_point = recent_df['Low'].min()
        
        diff = high_point - low_point
        
        fib_levels = {
            'high': high_point,
            'low': low_point,
            '0.382': high_point - (diff * 0.382),
            '0.5': high_point - (diff * 0.5),
            '0.618': high_point - (diff * 0.618),
            'current_price': df['Close'].iloc[-1]
        }
        
        return fib_levels

    def detect_support_resistance(self, df: pd.DataFrame, window: int = 20) -> Dict:
        df['Local_Max'] = df['High'].rolling(window=window, center=True).max()
        df['Local_Min'] = df['Low'].rolling(window=window, center=True).min()
        
        resistance_levels = df[df['High'] == df['Local_Max']]['High'].tail(5).tolist()
        support_levels = df[df['Low'] == df['Local_Min']]['Low'].tail(5).tolist()
        
        current_price = df['Close'].iloc[-1]
        
        return {
            'resistance': sorted(resistance_levels, reverse=True),
            'support': sorted(support_levels),
            'current_price': current_price,
            'nearest_resistance': min([r for r in resistance_levels if r > current_price], default=None),
            'nearest_support': max([s for s in support_levels if s < current_price], default=None)
        }

    def analyze_trend(self, df: pd.DataFrame) -> Dict:
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        trend_score = 0
        trend_signals = []
        
        if latest['MA5'] > latest['MA20']:
            trend_score += 10
            trend_signals.append('短期均线向上')
        if latest['MA20'] > latest['MA60']:
            trend_score += 10
            trend_signals.append('中期均线向上')
        if latest['MA60'] > latest['MA120']:
            trend_score += 10
            trend_signals.append('长期均线向上')
        if latest['Close'] > latest['MA5'] > latest['MA20']:
            trend_score += 15
            trend_signals.append('价格站上均线')
        
        if latest['Close'] > prev['Close']:
            trend_score += 5
            trend_signals.append('价格上涨')
        
        if trend_score >= 30:
            trend = '强势上升'
        elif trend_score >= 15:
            trend = '温和上升'
        elif trend_score >= -15:
            trend = '震荡整理'
        elif trend_score >= -30:
            trend = '温和下跌'
        else:
            trend = '强势下跌'
        
        return {
            'trend': trend,
            'score': trend_score,
            'signals': trend_signals
        }

    def analyze_momentum(self, df: pd.DataFrame) -> Dict:
        latest = df.iloc[-1]
        
        momentum_score = 0
        momentum_signals = []
        
        if 'RSI' in df.columns:
            rsi = latest['RSI']
            if rsi < 30:
                momentum_score += 15
                momentum_signals.append(f'RSI超卖({rsi:.1f})')
            elif rsi < 40:
                momentum_score += 10
                momentum_signals.append(f'RSI偏弱({rsi:.1f})')
            elif rsi > 70:
                momentum_score -= 15
                momentum_signals.append(f'RSI超买({rsi:.1f})')
            elif rsi > 60:
                momentum_score -= 10
                momentum_signals.append(f'RSI偏强({rsi:.1f})')
        
        if 'MACD_HIST' in df.columns and len(df) > 1:
            macd_hist = latest['MACD_HIST']
            prev_macd_hist = df['MACD_HIST'].iloc[-2]
            if macd_hist > 0 and prev_macd_hist <= 0:
                momentum_score += 20
                momentum_signals.append('MACD金叉')
            elif macd_hist < 0 and prev_macd_hist >= 0:
                momentum_score -= 20
                momentum_signals.append('MACD死叉')
            elif macd_hist > 0:
                momentum_score += 10
                momentum_signals.append('MACD柱状图为正')
            else:
                momentum_score -= 10
                momentum_signals.append('MACD柱状图为负')
        
        if '%K' in df.columns:
            k = latest['%K']
            d = latest['%D']
            if k < 20 and d < 20:
                momentum_score += 15
                momentum_signals.append('随机指标超卖')
            elif k > 80 and d > 80:
                momentum_score -= 15
                momentum_signals.append('随机指标超买')
            elif k > d:
                momentum_score += 5
                momentum_signals.append('随机指标向上')
        
        if 'Williams_R' in df.columns:
            wr = latest['Williams_R']
            if wr < -80:
                momentum_score += 10
                momentum_signals.append('威廉指标超卖')
            elif wr > -20:
                momentum_score -= 10
                momentum_signals.append('威廉指标超买')
        
        if momentum_score >= 30:
            momentum = '强劲'
        elif momentum_score >= 15:
            momentum = '向上'
        elif momentum_score >= -15:
            momentum = '中性'
        elif momentum_score >= -30:
            momentum = '向下'
        else:
            momentum = '疲弱'
        
        return {
            'momentum': momentum,
            'score': momentum_score,
            'signals': momentum_signals
        }

    def analyze_volume(self, df: pd.DataFrame) -> Dict:
        latest = df.iloc[-1]
        
        volume_score = 0
        volume_signals = []
        
        if 'Volume_Ratio' in df.columns:
            volume_ratio = latest['Volume_Ratio']
            if volume_ratio > 2:
                volume_score += 15
                volume_signals.append(f'放量({volume_ratio:.1f}倍)')
            elif volume_ratio > 1.5:
                volume_score += 10
                volume_signals.append(f'成交量放大({volume_ratio:.1f}倍)')
            elif volume_ratio < 0.5:
                volume_score -= 10
                volume_signals.append(f'缩量({volume_ratio:.1f}倍)')
        
        if 'OBV' in df.columns and len(df) > 1:
            obv = latest['OBV']
            prev_obv = df['OBV'].iloc[-2]
            if obv > prev_obv:
                volume_score += 5
                volume_signals.append('OBV向上')
            else:
                volume_score -= 5
                volume_signals.append('OBV向下')
        
        price_change = df['Close'].pct_change().iloc[-1]
        if 'Volume' in df.columns and len(df) > 1:
            volume_change = df['Volume'].pct_change().iloc[-1]
            
            if price_change > 0 and volume_change > 0:
                volume_score += 10
                volume_signals.append('量价齐升')
            elif price_change < 0 and volume_change > 0:
                volume_score -= 5
                volume_signals.append('放量下跌')
            elif price_change > 0 and volume_change < 0:
                volume_score -= 5
                volume_signals.append('缩量上涨')
        
        if volume_score >= 20:
            volume = '强劲'
        elif volume_score >= 10:
            volume = '良好'
        elif volume_score >= -10:
            volume = '正常'
        else:
            volume = '疲弱'
        
        return {
            'volume': volume,
            'score': volume_score,
            'signals': volume_signals
        }

    def analyze_volatility(self, df: pd.DataFrame) -> Dict:
        latest = df.iloc[-1]
        
        volatility_score = 0
        volatility_signals = []
        
        if 'ATR' in df.columns:
            atr = latest['ATR']
            atr_ma = df['ATR'].rolling(window=20).mean().iloc[-1]
            atr_ratio = atr / atr_ma if atr_ma > 0 else 1
            
            if atr_ratio > 1.5:
                volatility_score += 10
                volatility_signals.append(f'波动率上升({atr_ratio:.1f}倍)')
            elif atr_ratio < 0.7:
                volatility_score -= 10
                volatility_signals.append(f'波动率下降({atr_ratio:.1f}倍)')
        
        if 'BB_WIDTH' in df.columns:
            bb_width = latest['BB_WIDTH']
            bb_width_ma = df['BB_WIDTH'].rolling(window=20).mean().iloc[-1]
            
            if bb_width > bb_width_ma * 1.3:
                volatility_score += 10
                volatility_signals.append('布林带开口扩大')
            elif bb_width < bb_width_ma * 0.7:
                volatility_score -= 10
                volatility_signals.append('布林带开口收窄')
        
        returns = df['Close'].pct_change().tail(20)
        if not returns.empty:
            volatility_value = returns.std() * np.sqrt(252) * 100
            if volatility_value > 30:
                volatility_signals.append(f'年化波动率高({volatility_value:.1f}%)')
            elif volatility_value < 15:
                volatility_signals.append(f'年化波动率低({volatility_value:.1f}%)')
        
        if volatility_score >= 15:
            volatility = '高'
        elif volatility_score >= -15:
            volatility = '中等'
        else:
            volatility = '低'
        
        return {
            'volatility': volatility,
            'score': volatility_score,
            'signals': volatility_signals
        }

    def generate_comprehensive_signal(self, df: pd.DataFrame) -> Dict:
        if df.empty or len(df) < 120:
            return {}
        
        df = self.calculate_moving_averages(df)
        df = self.calculate_rsi(df)
        df = self.calculate_stochastic(df)
        df = self.calculate_macd(df)
        df = self.calculate_bollinger_bands(df)
        df = self.calculate_atr(df)
        df = self.calculate_cci(df)
        df = self.calculate_williams_r(df)
        df = self.calculate_volume_indicators(df)
        df = self.calculate_momentum(df)
        
        trend_analysis = self.analyze_trend(df)
        momentum_analysis = self.analyze_momentum(df)
        volume_analysis = self.analyze_volume(df)
        volatility_analysis = self.analyze_volatility(df)
        
        fib_levels = self.calculate_fibonacci_retracement(df)
        sr_levels = self.detect_support_resistance(df)
        
        total_score = (
            trend_analysis['score'] +
            momentum_analysis['score'] +
            volume_analysis['score'] +
            volatility_analysis['score']
        )
        
        if total_score >= 60:
            signal = '强烈买入'
            action = '考虑建仓'
        elif total_score >= 30:
            signal = '买入'
            action = '逢低买入'
        elif total_score >= 0:
            signal = '持有'
            action = '继续持有'
        elif total_score >= -30:
            signal = '观望'
            action = '谨慎观望'
        elif total_score >= -60:
            signal = '卖出'
            action = '逢高减仓'
        else:
            signal = '强烈卖出'
            action = '考虑清仓'
        
        latest = df.iloc[-1]
        
        return {
            'overall_signal': signal,
            'action': action,
            'total_score': total_score,
            'trend': trend_analysis,
            'momentum': momentum_analysis,
            'volume': volume_analysis,
            'volatility': volatility_analysis,
            'fibonacci': fib_levels,
            'support_resistance': sr_levels,
            'current_data': {
                'price': latest['Close'],
                'ma5': latest['MA5'],
                'ma20': latest['MA20'],
                'ma60': latest['MA60'],
                'rsi': latest['RSI'],
                'macd': latest['MACD'],
                'macd_hist': latest['MACD_HIST'],
                'bb_upper': latest['BB_UPPER'],
                'bb_middle': latest['BB_MIDDLE'],
                'bb_lower': latest['BB_LOWER'],
                'atr': latest['ATR'],
                'cci': latest['CCI'],
                'williams_r': latest['Williams_R'],
                'stoch_k': latest['%K'],
                'stoch_d': latest['%D'],
                'volume': latest['Volume'],
                'volume_ratio': latest.get('Volume_Ratio', 0)
            }
        }
