import sys
import os
import time
import json
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


class StockAnalyzer:
    def __init__(self):
        self.cn_fetcher = ChinaStockFetcher()
        self.hk_fetcher = HongKongStockFetcher()
        self.us_fetcher = USStockFetcher()
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.technical_analyzer = AdvancedTechnicalAnalyzer()
        self.recommender = Recommender()
        self.report_generator = ReportGenerator()
        self.data_dir = 'data'

    def load_data(self, filepath: str) -> Dict:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"数据加载成功: {filepath}")
            return data
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
            return {}

    def get_latest_data_file(self) -> str:
        try:
            files = [f for f in os.listdir(self.data_dir) if f.startswith('market_data_') and f.endswith('.json')]
            if not files:
                logger.error("未找到数据文件")
                return ""
            
            files.sort(reverse=True)
            return os.path.join(self.data_dir, files[0])
        except Exception as e:
            logger.error(f"查找最新数据文件失败: {e}")
            return ""

    def analyze_stock(self, stock_info: Dict, market: str) -> Dict:
        try:
            code = stock_info.get('代码') or stock_info.get('code', '')
            name = stock_info.get('名称') or stock_info.get('name', '')
            
            if not code:
                return None
            
            stock_data = stock_info.copy()
            
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
                logger.info(f"完成分析: {name} ({code}), 评分: {recommendation['total_score']}")
            
            return recommendation
        except Exception as e:
            logger.error(f"分析股票失败: {e}")
            return None

    def analyze_market_stocks(self, market_data: Dict) -> List[Dict]:
        market = market_data.get('market', '')
        stocks_to_analyze = market_data.get('stocks_to_analyze', [])
        
        logger.info(f"开始分析 {market} 市场 {len(stocks_to_analyze)} 只股票")
        
        recommendations = []
        
        for idx, stock in enumerate(stocks_to_analyze):
            if idx > 0 and idx % 5 == 0:
                time.sleep(1)
            
            recommendation = self.analyze_stock(stock, market)
            
            if recommendation:
                recommendations.append(recommendation)
        
        logger.info(f"{market} 市场分析完成，共 {len(recommendations)} 只股票")
        return recommendations

    def analyze_all_stocks(self, data: Dict) -> Dict:
        logger.info("=" * 50)
        logger.info("开始执行股票分析")
        logger.info("=" * 50)
        
        all_recommendations = {
            'timestamp': datetime.now().isoformat(),
            'cn': [],
            'hk': [],
            'us': []
        }
        
        cn_data = data.get('cn', {})
        if cn_data:
            cn_recommendations = self.analyze_market_stocks(cn_data)
            all_recommendations['cn'] = cn_recommendations
        
        hk_data = data.get('hk', {})
        if hk_data:
            hk_recommendations = self.analyze_market_stocks(hk_data)
            all_recommendations['hk'] = hk_recommendations
        
        us_data = data.get('us', {})
        if us_data:
            us_recommendations = self.analyze_market_stocks(us_data)
            all_recommendations['us'] = us_recommendations
        
        return all_recommendations

    def save_recommendations(self, recommendations: Dict, filename: str = None) -> str:
        try:
            if not filename:
                filename = f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            filepath = os.path.join(self.data_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(recommendations, f, ensure_ascii=False, indent=2)
            
            logger.info(f"推荐数据已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存推荐数据失败: {e}")
            return ""

    def generate_report(self, market_data: Dict, recommendations: Dict) -> str:
        logger.info("开始生成投资报告...")
        try:
            cn_data = market_data.get('cn', {})
            hk_data = market_data.get('hk', {})
            us_data = market_data.get('us', {})
            
            all_recommendations = []
            all_recommendations.extend(recommendations.get('cn', []))
            all_recommendations.extend(recommendations.get('hk', []))
            all_recommendations.extend(recommendations.get('us', []))
            
            top_recommendations = self.recommender.select_top_stocks(all_recommendations, top_n=10)
            
            html_content = self.report_generator.generate_html_report(
                cn_data, hk_data, us_data, top_recommendations
            )
            
            if html_content:
                filepath = self.report_generator.save_report(html_content)
                logger.info(f"报告已生成: {filepath}")
                return filepath
            return ""
        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            return ""

    def send_email_report(self, report_path: str, email_config: Dict) -> bool:
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

    def run(self, data_file: str = None):
        if not data_file:
            data_file = self.get_latest_data_file()
        
        if not data_file:
            logger.error("无法加载数据文件")
            return False
        
        market_data = self.load_data(data_file)
        
        if not market_data:
            logger.error("数据加载失败")
            return False
        
        recommendations = self.analyze_all_stocks(market_data)
        
        self.save_recommendations(recommendations)
        
        report_path = self.generate_report(market_data, recommendations)
        
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
        logger.info("股票分析完成")
        logger.info("=" * 50)
        return True


if __name__ == "__main__":
    import sys
    data_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    analyzer = StockAnalyzer()
    analyzer.run(data_file)
