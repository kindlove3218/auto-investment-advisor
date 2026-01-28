import sys
import os
import time
import json
import logging
from datetime import datetime
from typing import Dict
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.fetchers.china_fetcher import ChinaStockFetcher
from src.fetchers.hk_fetcher import HongKongStockFetcher
from src.fetchers.us_fetcher import USStockFetcher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataFetcher:
    def __init__(self):
        self.cn_fetcher = ChinaStockFetcher()
        self.hk_fetcher = HongKongStockFetcher()
        self.us_fetcher = USStockFetcher()
        self.output_dir = 'data'
        
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_china_data(self) -> Dict:
        logger.info("开始获取中国股市数据...")
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'market': 'cn',
                'hot_stocks': {},
                'hot_sectors': [],
                'stocks_to_analyze': []
            }
            
            try:
                hot_stocks = self.cn_fetcher.get_hot_stocks()
                time.sleep(1)
                
                if hot_stocks:
                    data['hot_stocks']['top_gainers'] = hot_stocks.get('top_gainers', pd.DataFrame()).head(50).to_dict('records')
                    data['hot_stocks']['top_losers'] = hot_stocks.get('top_losers', pd.DataFrame()).head(50).to_dict('records')
                    data['hot_stocks']['top_volume'] = hot_stocks.get('top_volume', pd.DataFrame()).head(50).to_dict('records')
                    
                    data['stocks_to_analyze'].extend(
                        stock.to_dict() for stock in hot_stocks.get('top_gainers', pd.DataFrame()).head(20).itertuples()
                    )
            except Exception as e:
                logger.warning(f"获取热门股票失败: {e}")
            
            try:
                hot_sectors = self.cn_fetcher.get_hot_sectors()
                time.sleep(1)
                
                if not hot_sectors.empty:
                    data['hot_sectors'] = hot_sectors.head(20).to_dict('records')
            except Exception as e:
                logger.warning(f"获取热门板块失败: {e}")
            
            logger.info(f"获取到 {len(data['stocks_to_analyze'])} 只A股待分析")
            return data
        except Exception as e:
            logger.error(f"获取中国股市数据失败: {e}")
            return {}

    def fetch_hk_data(self) -> Dict:
        logger.info("开始获取港股数据...")
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'market': 'hk',
                'hot_stocks': {},
                'stocks_to_analyze': []
            }
            
            try:
                hot_stocks = self.hk_fetcher.get_hot_stocks()
                time.sleep(1)
                
                if hot_stocks:
                    data['hot_stocks']['top_gainers'] = hot_stocks.get('top_gainers', pd.DataFrame()).head(50).to_dict('records')
                    data['hot_stocks']['top_losers'] = hot_stocks.get('top_losers', pd.DataFrame()).head(50).to_dict('records')
                    data['hot_stocks']['top_volume'] = hot_stocks.get('top_volume', pd.DataFrame()).head(50).to_dict('records')
                    
                    data['stocks_to_analyze'].extend(
                        stock.to_dict() for stock in hot_stocks.get('top_gainers', pd.DataFrame()).head(15).itertuples()
                    )
            except Exception as e:
                logger.warning(f"获取热门港股失败: {e}")
            
            logger.info(f"获取到 {len(data['stocks_to_analyze'])} 只港股待分析")
            return data
        except Exception as e:
            logger.error(f"获取港股数据失败: {e}")
            return {}

    def fetch_us_data(self) -> Dict:
        logger.info("开始获取美股数据...")
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'market': 'us',
                'hot_stocks': [],
                'sector_performance': [],
                'stocks_to_analyze': []
            }
            
            try:
                hot_stocks = self.us_fetcher.get_hot_stocks()
                time.sleep(1)
                
                if not hot_stocks.empty:
                    data['hot_stocks'] = hot_stocks.head(50).to_dict('records')
                    
                    data['stocks_to_analyze'].extend(
                        stock.to_dict() for stock in hot_stocks.head(15).itertuples()
                    )
            except Exception as e:
                logger.warning(f"获取热门美股失败: {e}")
            
            try:
                sector_performance = self.us_fetcher.get_sector_performance()
                time.sleep(1)
                
                if not sector_performance.empty:
                    data['sector_performance'] = sector_performance.to_dict('records')
            except Exception as e:
                logger.warning(f"获取板块表现失败: {e}")
            
            logger.info(f"获取到 {len(data['stocks_to_analyze'])} 只美股待分析")
            return data
        except Exception as e:
            logger.error(f"获取美股数据失败: {e}")
            return {}

    def fetch_all_data(self) -> Dict:
        logger.info("=" * 50)
        logger.info("开始执行数据获取")
        logger.info("=" * 50)
        
        all_data = {
            'timestamp': datetime.now().isoformat(),
            'cn': self.fetch_china_data(),
            'hk': self.fetch_hk_data(),
            'us': self.fetch_us_data()
        }
        
        return all_data

    def save_data(self, data: Dict, filename: str = None) -> str:
        try:
            if not filename:
                filename = f"market_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"数据已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存数据失败: {e}")
            return ""

    def run(self):
        data = self.fetch_all_data()
        filepath = self.save_data(data)
        
        if filepath:
            logger.info("=" * 50)
            logger.info("数据获取完成")
            logger.info(f"数据文件: {filepath}")
            logger.info("=" * 50)
            return filepath
        else:
            logger.error("数据获取失败")
            return None


if __name__ == "__main__":
    fetcher = DataFetcher()
    fetcher.run()
