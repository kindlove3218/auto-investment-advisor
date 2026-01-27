import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChinaStockFetcher:
    def __init__(self):
        pass

    def get_index_data(self, index_code, start_date=None):
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            
            df = ak.stock_zh_index_daily(symbol=index_code)
            df.index = pd.to_datetime(df.index)
            return df
        except Exception as e:
            logger.error(f"获取指数数据失败 {index_code}: {e}")
            return pd.DataFrame()

    def get_all_stocks(self):
        try:
            df = ak.stock_zh_a_spot_em()
            return df
        except Exception as e:
            logger.error(f"获取A股列表失败: {e}")
            return pd.DataFrame()

    def get_stock_data(self, stock_code, start_date=None):
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            
            df = ak.stock_zh_a_daily(symbol=stock_code, start_date=start_date)
            return df
        except Exception as e:
            logger.error(f"获取股票数据失败 {stock_code}: {e}")
            return pd.DataFrame()

    def get_hot_stocks(self):
        try:
            df = ak.stock_zh_a_spot_em()
            
            df = df.sort_values('涨跌幅', ascending=False)
            
            top_gainers = df.head(20)
            top_losers = df.tail(20)
            
            top_volume = df.sort_values('成交量', ascending=False).head(20)
            
            return {
                "top_gainers": top_gainers,
                "top_losers": top_losers,
                "top_volume": top_volume
            }
        except Exception as e:
            logger.error(f"获取热门股票失败: {e}")
            return {}

    def get_hot_sectors(self):
        try:
            df = ak.stock_board_industry_name_em()
            return df
        except Exception as e:
            logger.error(f"获取热门板块失败: {e}")
            return pd.DataFrame()

    def get_sector_stocks(self, sector_name):
        try:
            df = ak.stock_board_industry_cons_em(symbol=sector_name)
            return df
        except Exception as e:
            logger.error(f"获取板块股票失败 {sector_name}: {e}")
            return pd.DataFrame()
