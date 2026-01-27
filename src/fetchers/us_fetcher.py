import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class USStockFetcher:
    def __init__(self):
        pass

    def get_index_data(self, index_code, start_date=None):
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365))
            
            df = yf.download(index_code, start=start_date)
            return df
        except Exception as e:
            logger.error(f"获取美股指数数据失败 {index_code}: {e}")
            return pd.DataFrame()

    def get_stock_data(self, stock_code, start_date=None):
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365))
            
            df = yf.download(stock_code, start=start_date)
            return df
        except Exception as e:
            logger.error(f"获取美股数据失败 {stock_code}: {e}")
            return pd.DataFrame()

    def get_stock_info(self, stock_code):
        try:
            ticker = yf.Ticker(stock_code)
            info = ticker.info
            return info
        except Exception as e:
            logger.error(f"获取股票信息失败 {stock_code}: {e}")
            return {}

    def get_hot_stocks(self, top_n=20):
        try:
            popular_tickers = [
                "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA",
                "BRK-B", "LLY", "AVGO", "JPM", "XOM", "MA", "HD", "PG",
                "COST", "MRK", "CVX", "KO", "PEP"
            ]
            
            hot_stocks_data = []
            for ticker in popular_tickers[:top_n]:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    hist = stock.history(period="5d")
                    
                    if not hist.empty:
                        latest_price = hist['Close'].iloc[-1]
                        prev_close = hist['Close'].iloc[-2]
                        change_percent = ((latest_price - prev_close) / prev_close) * 100
                        
                        hot_stocks_data.append({
                            '代码': ticker,
                            '名称': info.get('longName', ticker),
                            '价格': latest_price,
                            '涨跌幅': change_percent,
                            '成交量': hist['Volume'].iloc[-1],
                            '市值': info.get('marketCap', 0)
                        })
                except:
                    continue
            
            df = pd.DataFrame(hot_stocks_data)
            return df
        except Exception as e:
            logger.error(f"获取热门美股失败: {e}")
            return pd.DataFrame()

    def get_sector_performance(self):
        try:
            sector_etfs = {
                "Technology": "XLK",
                "Financial": "XLF",
                "Healthcare": "XLV",
                "Consumer": "XLY",
                "Energy": "XLE",
                "Industrial": "XLI",
                "Utilities": "XLU",
                "Real Estate": "XLRE"
            }
            
            sector_data = []
            for sector, ticker in sector_etfs.items():
                try:
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period="5d")
                    
                    if not hist.empty:
                        latest = hist['Close'].iloc[-1]
                        prev = hist['Close'].iloc[-2]
                        change = ((latest - prev) / prev) * 100
                        
                        sector_data.append({
                            '板块': sector,
                            '涨跌幅': change
                        })
                except:
                    continue
            
            df = pd.DataFrame(sector_data)
            return df
        except Exception as e:
            logger.error(f"获取美股板块表现失败: {e}")
            return pd.DataFrame()
