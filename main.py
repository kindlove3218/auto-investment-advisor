import sys
import os
import time
import logging
from datetime import datetime
from typing import Dict, List

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.fetchers.china_fetcher import ChinaStockFetcher
from src.fetchers.hk_fetcher import HongKongStockFetcher
from src.fetchers.us_fetcher import USStockFetcher
from src.analyzers.fundamental_analyzer import FundamentalAnalyzer
from src.analyzers.advanced_technical_analyzer import AdvancedTechnicalAnalyzer
from src.recommenders.recommender import Recommender
from src.reporters.report_generator import ReportGenerator
from src.utils.email_sender import EmailSender

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InvestmentAdvisor:
    def __init__(self):
        self.cn_fetcher = ChinaStockFetcher()
        self.hk_fetcher = HongKongStockFetcher()
        self.us_fetcher = USStockFetcher()
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.technical_analyzer = AdvancedTechnicalAnalyzer()
        self.recommender = Recommender()
        self.report_generator = ReportGenerator()
        
    def fetch_china_data(self) -> Dict:
        logger.info("开始获取中国股市数据...")
        try:
            data = {}
            
            hot_stocks = self.cn_fetcher.get_hot_stocks()
            time.sleep(1)
            
            hot_sectors = self.cn_fetcher.get_hot_sectors()
            time.sleep(1)
            
            data['hot_stocks'] = hot_stocks
            data['hot_sectors'] = hot_sectors
            
            logger.info(f"获取到 {len(hot_stocks.get('top_gainers', []))} 只热门A股")
            return data
        except Exception as e:
            logger.error(f"获取中国股市数据失败: {e}")
            return {}

    def fetch_hk_data(self) -> Dict:
        logger.info("开始获取港股数据...")
        try:
            data = {}
            
            hot_stocks = self.hk_fetcher.get_hot_stocks()
            time.sleep(1)
            
            data['hot_stocks'] = hot_stocks
            
            logger.info(f"获取到 {len(hot_stocks.get('top_gainers', []))} 只热门港股")
            return data
        except Exception as e:
            logger.error(f"获取港股数据失败: {e}")
            return {}

    def fetch_us_data(self) -> Dict:
        logger.info("开始获取美股数据...")
        try:
            data = {}
            
            hot_stocks = self.us_fetcher.get_hot_stocks()
            time.sleep(1)
            
            sector_performance = self.us_fetcher.get_sector_performance()
            time.sleep(1)
            
            data['hot_stocks'] = hot_stocks
            data['sector_performance'] = sector_performance
            
            logger.info(f"获取到 {len(hot_stocks)} 只热门美股")
            return data
        except Exception as e:
            logger.error(f"获取美股数据失败: {e}")
            return {}

    def analyze_stocks(self, stocks: List[Dict], market: str) -> List[Dict]:
        logger.info(f"开始分析{market}股票...")
        recommendations = []
        
        for idx, stock in enumerate(stocks[:20]):
            try:
                code = stock.get('代码', '')
                name = stock.get('名称', '')
                
                if not code:
                    continue
                
                if idx > 0 and idx % 5 == 0:
                    time.sleep(1)
                
                stock_data = stock.to_dict() if hasattr(stock, 'to_dict') else stock
                
                fundamental_analysis = self.fundamental_analyzer.analyze_stock(stock_data)
                
                historical_data = None
                if market == 'cn':
                    historical_data = self.cn_fetcher.get_stock_data(code)
                elif market == 'hk':
                    historical_data = self.hk_fetcher.get_stock_data(code)
                elif market == 'us':
                    historical_data = self.us_fetcher.get_stock_data(code)
                
                technical_analysis = {}
                if historical_data is not None and not historical_data.empty:
                    technical_analysis = self.technical_analyzer.generate_comprehensive_signal(historical_data)
                
                recommendation = self.recommender.generate_recommendation(
                    code, name, fundamental_analysis, technical_analysis
                )
                
                if recommendation:
                    recommendations.append(recommendation)
                
            except Exception as e:
                logger.error(f"分析股票 {stock.get('代码', '')} 失败: {e}")
                continue
        
        logger.info(f"完成{market}股票分析，共{len(recommendations)}只")
        return recommendations

    def generate_report(self, cn_data: Dict, hk_data: Dict, us_data: Dict, 
                        recommendations: List[Dict]) -> str:
        logger.info("开始生成投资报告...")
        try:
            html_content = self.report_generator.generate_html_report(
                cn_data, hk_data, us_data, recommendations
            )
            
            if html_content:
                filepath = self.report_generator.save_report(html_content)
                logger.info(f"报告已生成: {filepath}")
                return filepath
            return ""
        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            return ""

    def send_email_report(self, report_path: str, email_config: Dict):
        logger.info("开始发送邮件报告...")
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                report_content = f.read()
            
            email_sender = EmailSender(
                smtp_server=email_config['smtp_server'],
                smtp_port=email_config['smtp_port'],
                sender=email_config['sender'],
                password=email_config['password']
            )
            
            success = email_sender.send_investment_report(
                receiver=email_config['receiver'],
                report_content=report_content,
                html=True
            )
            
            if success:
                logger.info("邮件发送成功")
            else:
                logger.error("邮件发送失败")
            
            return success
        except Exception as e:
            logger.error(f"发送邮件失败: {e}")
            return False

    def run(self):
        logger.info("=" * 50)
        logger.info("开始执行投资顾问系统")
        logger.info("=" * 50)
        
        cn_data = self.fetch_china_data()
        
        hk_data = self.fetch_hk_data()
        
        us_data = self.fetch_us_data()
        
        recommendations = []
        
        if cn_data and cn_data.get('hot_stocks', {}).get('top_gainers') is not None:
            top_gainers = cn_data['hot_stocks']['top_gainers']
            cn_recommendations = self.analyze_stocks(top_gainers, 'cn')
            recommendations.extend(cn_recommendations)
        
        if hk_data and hk_data.get('hot_stocks', {}).get('top_gainers') is not None:
            top_gainers = hk_data['hot_stocks']['top_gainers']
            hk_recommendations = self.analyze_stocks(top_gainers, 'hk')
            recommendations.extend(hk_recommendations)
        
        if us_data and not us_data.get('hot_stocks').empty:
            hot_stocks = us_data['hot_stocks']
            us_recommendations = self.analyze_stocks(hot_stocks, 'us')
            recommendations.extend(us_recommendations)
        
        top_recommendations = self.recommender.select_top_stocks(recommendations, top_n=10)
        
        report_path = self.generate_report(cn_data, hk_data, us_data, top_recommendations)
        
        if report_path:
            from dotenv import load_dotenv
            load_dotenv()
            
            email_config = {
                'smtp_server': os.getenv('EMAIL_SMTP_SERVER'),
                'smtp_port': int(os.getenv('EMAIL_SMTP_PORT', 587)),
                'sender': os.getenv('EMAIL_SENDER'),
                'password': os.getenv('EMAIL_PASSWORD'),
                'receiver': os.getenv('EMAIL_RECEIVER')
            }
            
            if email_config['sender'] and email_config['password']:
                self.send_email_report(report_path, email_config)
        
        logger.info("=" * 50)
        logger.info("投资顾问系统执行完成")
        logger.info("=" * 50)


if __name__ == "__main__":
    advisor = InvestmentAdvisor()
    advisor.run()
