import time
import pandas as pd
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Recommender:
    def __init__(self):
        self.buy_threshold = 0.7
        self.sell_threshold = 0.3
        self.min_score = 60

    def generate_recommendation(self, stock_code: str, stock_name: str, 
                               fundamental_analysis: Dict, 
                               technical_analysis: Dict) -> Dict:
        try:
            recommendation = {
                'code': stock_code,
                'name': stock_name,
                'fundamental_score': 0,
                'technical_score': 0,
                'total_score': 0,
                'rating': '持有',
                'action': '观望',
                'target_price': None,
                'stop_loss': None,
                'risk_level': '中等',
                'holding_period': '中期',
                'reasons': []
            }
            
            if fundamental_analysis:
                recommendation['fundamental_score'] = fundamental_analysis.get('total_score', 0)
                
                pe_score = fundamental_analysis.get('pe_score', '')
                if pe_score == '合理':
                    recommendation['reasons'].append('估值合理')
                elif pe_score == '偏低':
                    recommendation['reasons'].append('估值偏低')
                
                roe_score = fundamental_analysis.get('roe_score', '')
                if roe_score == '优秀':
                    recommendation['reasons'].append('ROE优秀')
                elif roe_score == '良好':
                    recommendation['reasons'].append('ROE良好')
                
                revenue_growth = fundamental_analysis.get('revenue_growth_score', '')
                if revenue_growth == '优秀':
                    recommendation['reasons'].append('营收增长优秀')
                elif revenue_growth == '良好':
                    recommendation['reasons'].append('营收增长良好')
            
            if technical_analysis:
                recommendation['technical_score'] = technical_analysis.get('total_score', 0)
                
                trend = technical_analysis.get('trend', {})
                if trend.get('trend') in ['强势上升', '温和上升']:
                    recommendation['reasons'].append(f"趋势{trend.get('trend')}")
                
                momentum = technical_analysis.get('momentum', {})
                if momentum.get('momentum') in ['强劲', '向上']:
                    recommendation['reasons'].append(f"动能{momentum.get('momentum')}")
                
                volume = technical_analysis.get('volume', {})
                if volume.get('volume') in ['强劲', '良好']:
                    recommendation['reasons'].append(f"成交量{volume.get('volume')}")
                
                current_data = technical_analysis.get('current_data', {})
                if 'price' in current_data:
                    recommendation['current_price'] = current_data['price']
                
                if 'atr' in current_data:
                    stop_loss = current_data['price'] * (1 - current_data['atr'] * 2 / current_data['price'])
                    recommendation['stop_loss'] = round(stop_loss, 2)
                
                sr = technical_analysis.get('support_resistance', {})
                if 'nearest_resistance' in sr and sr['nearest_resistance']:
                    recommendation['target_price'] = round(sr['nearest_resistance'], 2)
                elif 'nearest_support' in sr and sr['nearest_support']:
                    target = current_data.get('price', 0) * 1.15
                    recommendation['target_price'] = round(target, 2)
            
            recommendation['total_score'] = int((recommendation['fundamental_score'] + recommendation['technical_score']) / 2)
            
            if recommendation['total_score'] >= 80:
                recommendation['rating'] = '强烈推荐'
                recommendation['action'] = '建议买入'
                recommendation['risk_level'] = '低'
                recommendation['holding_period'] = '长期'
            elif recommendation['total_score'] >= 70:
                recommendation['rating'] = '推荐'
                recommendation['action'] = '建议买入'
                recommendation['risk_level'] = '中低'
                recommendation['holding_period'] = '中长期'
            elif recommendation['total_score'] >= 60:
                recommendation['rating'] = '观望'
                recommendation['action'] = '逢低关注'
                recommendation['risk_level'] = '中等'
                recommendation['holding_period'] = '中期'
            elif recommendation['total_score'] >= 50:
                recommendation['rating'] = '中性'
                recommendation['action'] = '谨慎持有'
                recommendation['risk_level'] = '中等偏高'
                recommendation['holding_period'] = '短期'
            else:
                recommendation['rating'] = '不推荐'
                recommendation['action'] = '建议规避'
                recommendation['risk_level'] = '高'
                recommendation['holding_period'] = '不适用'
            
            return recommendation
        except Exception as e:
            logger.error(f"生成推荐失败: {e}")
            return {}

    def select_top_stocks(self, recommendations: List[Dict], top_n: int = 10) -> List[Dict]:
        try:
            sorted_recs = sorted(recommendations, key=lambda x: x.get('total_score', 0), reverse=True)
            return sorted_recs[:top_n]
        except Exception as e:
            logger.error(f"筛选热门股票失败: {e}")
            return []

    def generate_portfolio_suggestion(self, recommendations: List[Dict]) -> Dict:
        try:
            buy_recs = [r for r in recommendations if r.get('total_score', 0) >= 60]
            hold_recs = [r for r in recommendations if 50 <= r.get('total_score', 0) < 60]
            sell_recs = [r for r in recommendations if r.get('total_score', 0) < 50]
            
            suggestion = {
                'buy_count': len(buy_recs),
                'hold_count': len(hold_recs),
                'sell_count': len(sell_recs),
                'buy_recommendations': buy_recs[:5],
                'hold_recommendations': hold_recs[:5],
                'sell_recommendations': sell_recs[:5],
                'market_sentiment': '中性'
            }
            
            total_count = len(recommendations)
            if total_count > 0:
                buy_ratio = len(buy_recs) / total_count
                if buy_ratio > 0.6:
                    suggestion['market_sentiment'] = '乐观'
                elif buy_ratio > 0.4:
                    suggestion['market_sentiment'] = '偏乐观'
                elif buy_ratio > 0.2:
                    suggestion['market_sentiment'] = '中性'
                elif buy_ratio > 0.1:
                    suggestion['market_sentiment'] = '偏悲观'
                else:
                    suggestion['market_sentiment'] = '悲观'
            
            return suggestion
        except Exception as e:
            logger.error(f"生成投资组合建议失败: {e}")
            return {}
