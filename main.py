import sys
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    load_dotenv()
    
    logger.info("=" * 60)
    logger.info("       自动投资顾问系统 - 主程序")
    logger.info("=" * 60)
    
    mode = os.getenv('RUN_MODE', 'full').lower()
    
    if mode == 'fetch':
        logger.info("运行模式: 数据获取")
        from fetch_data import DataFetcher
        fetcher = DataFetcher()
        fetcher.run()
    
    elif mode == 'analyze':
        logger.info("运行模式: 股票分析")
        from analyze_stocks import StockAnalyzer
        analyzer = StockAnalyzer()
        analyzer.run()
    
    elif mode == 'full':
        logger.info("运行模式: 完整流程")
        from fetch_data import DataFetcher
        from analyze_stocks import StockAnalyzer
        
        fetcher = DataFetcher()
        data_file = fetcher.run()
        
        if data_file:
            analyzer = StockAnalyzer()
            analyzer.run(data_file)
    
    else:
        logger.error(f"未知的运行模式: {mode}")
        logger.info("可用模式: fetch, analyze, full")
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("程序执行完成")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
