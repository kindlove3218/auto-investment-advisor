import pandas as pd
import numpy as np
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FundamentalAnalyzer:
    def __init__(self):
        pass

    def analyze_stock(self, stock_data: Dict) -> Dict:
        try:
            score = 0
            analysis = {}
            
            pe_ratio = stock_data.get('pe_ratio', 0)
            pb_ratio = stock_data.get('pb_ratio', 0)
            roe = stock_data.get('roe', 0)
            revenue_growth = stock_data.get('revenue_growth', 0)
            profit_growth = stock_data.get('profit_growth', 0)
            
            if pe_ratio > 0 and pe_ratio < 30:
                score += 20
                analysis['pe_score'] = '合理'
            elif pe_ratio >= 30 and pe_ratio < 50:
                score += 10
                analysis['pe_score'] = '偏高'
            else:
                analysis['pe_score'] = '过高'
            
            if pb_ratio > 0 and pb_ratio < 3:
                score += 20
                analysis['pb_score'] = '合理'
            elif pb_ratio >= 3 and pb_ratio < 5:
                score += 10
                analysis['pb_score'] = '偏高'
            else:
                analysis['pb_score'] = '过高'
            
            if roe > 15:
                score += 20
                analysis['roe_score'] = '优秀'
            elif roe > 10:
                score += 15
                analysis['roe_score'] = '良好'
            elif roe > 5:
                score += 10
                analysis['roe_score'] = '一般'
            else:
                analysis['roe_score'] = '较差'
            
            if revenue_growth > 20:
                score += 20
                analysis['revenue_growth_score'] = '优秀'
            elif revenue_growth > 10:
                score += 15
                analysis['revenue_growth_score'] = '良好'
            elif revenue_growth > 0:
                score += 10
                analysis['revenue_growth_score'] = '一般'
            else:
                analysis['revenue_growth_score'] = '负增长'
            
            if profit_growth > 20:
                score += 20
                analysis['profit_growth_score'] = '优秀'
            elif profit_growth > 10:
                score += 15
                analysis['profit_growth_score'] = '良好'
            elif profit_growth > 0:
                score += 10
                analysis['profit_growth_score'] = '一般'
            else:
                analysis['profit_growth_score'] = '负增长'
            
            analysis['total_score'] = score
            analysis['rating'] = self._get_rating(score)
            
            return analysis
        except Exception as e:
            logger.error(f"基本面分析失败: {e}")
            return {}

    def _get_rating(self, score: int) -> str:
        if score >= 80:
            return '强烈推荐'
        elif score >= 70:
            return '推荐'
        elif score >= 60:
            return '观望'
        elif score >= 50:
            return '中性'
        else:
            return '不推荐'

    def analyze_market(self, market_data: pd.DataFrame) -> Dict:
        try:
            analysis = {
                'avg_pe': 0,
                'avg_pb': 0,
                'avg_roe': 0,
                'market_sentiment': '中性'
            }
            
            if 'pe_ratio' in market_data.columns:
                analysis['avg_pe'] = market_data['pe_ratio'].mean()
            if 'pb_ratio' in market_data.columns:
                analysis['avg_pb'] = market_data['pb_ratio'].mean()
            if 'roe' in market_data.columns:
                analysis['avg_roe'] = market_data['roe'].mean()
            
            if analysis['avg_pe'] < 15 and analysis['avg_pb'] < 2:
                analysis['market_sentiment'] = '低估'
            elif analysis['avg_pe'] > 30 and analysis['avg_pb'] > 4:
                analysis['market_sentiment'] = '高估'
            
            return analysis
        except Exception as e:
            logger.error(f"市场分析失败: {e}")
            return {}
