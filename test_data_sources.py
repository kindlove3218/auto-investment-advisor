"""
测试各个数据源
"""

import sys
import os
import logging
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_akshare():
    """测试 AKShare 连接"""
    logger.info("=" * 60)
    logger.info("测试 AKShare 数据源")
    logger.info("=" * 60)
    
    try:
        import akshare as ak
        
        # 测试 1: 获取 A 股热门股票
        logger.info("\n[测试 1] 获取 A 股热门股票...")
        try:
            df = ak.stock_zh_a_spot_em()
            if not df.empty:
                logger.info(f"✓ 成功获取 {len(df)} 只 A 股")
                logger.info(f"  前 3 只:")
                for idx, row in df.head(3).iterrows():
                    logger.info(f"    {row.get('代码', '')} - {row.get('名称', '')}")
            else:
                logger.warning("✗ 获取的 A 股数据为空")
        except Exception as e:
            logger.error(f"✗ 获取 A 股失败: {e}")
        
        time.sleep(2)
        
        # 测试 2: 获取热门板块
        logger.info("\n[测试 2] 获取热门板块...")
        try:
            df = ak.stock_board_industry_name_em()
            if not df.empty:
                logger.info(f"✓ 成功获取 {len(df)} 个板块")
                logger.info(f"  前 3 个:")
                for idx, row in df.head(3).iterrows():
                    logger.info(f"    {row.get('板块名称', '')} - {row.get('涨跌幅', 0):.2f}%")
            else:
                logger.warning("✗ 获取的板块数据为空")
        except Exception as e:
            logger.error(f"✗ 获取板块失败: {e}")
        
        time.sleep(2)
        
        # 测试 3: 获取港股
        logger.info("\n[测试 3] 获取港股...")
        try:
            df = ak.stock_hk_spot_em()
            if not df.empty:
                logger.info(f"✓ 成功获取 {len(df)} 只港股")
                logger.info(f"  前 3 只:")
                for idx, row in df.head(3).iterrows():
                    logger.info(f"    {row.get('代码', '')} - {row.get('名称', '')}")
            else:
                logger.warning("✗ 获取的港股数据为空")
        except Exception as e:
            logger.error(f"✗ 获取港股失败: {e}")
        
    except ImportError as e:
        logger.error(f"✗ AKShare 导入失败: {e}")
        return False
    
    return True


def test_yfinance():
    """测试 yFinance 连接"""
    logger.info("\n" + "=" * 60)
    logger.info("测试 yFinance 数据源")
    logger.info("=" * 60)
    
    try:
        import yfinance as yf
        from datetime import datetime, timedelta
        
        # 测试 1: 获取美股
        logger.info("\n[测试 1] 获取美股 Apple (AAPL)...")
        try:
            stock = yf.Ticker("AAPL")
            info = stock.info
            logger.info(f"✓ 成功获取 Apple 信息")
            logger.info(f"  名称: {info.get('longName', 'N/A')}")
            logger.info(f"  市值: {info.get('marketCap', 'N/A')}")
        except Exception as e:
            logger.error(f"✗ 获取 Apple 信息失败: {e}")
        
        time.sleep(2)
        
        # 测试 2: 获取历史数据
        logger.info("\n[测试 2] 获取历史数据...")
        try:
            start_date = datetime.now() - timedelta(days=30)
            df = yf.download("AAPL", start=start_date, progress=False)
            if not df.empty:
                logger.info(f"✓ 成功获取历史数据")
                logger.info(f"  数据行数: {len(df)}")
                logger.info(f"  最新价格: {df['Close'].iloc[-1]:.2f}")
            else:
                logger.warning("✗ 获取的历史数据为空")
        except Exception as e:
            logger.error(f"✗ 获取历史数据失败: {e}")
        
        time.sleep(2)
        
        # 测试 3: 获取多个股票
        logger.info("\n[测试 3] 批量获取热门股票...")
        try:
            tickers = ["AAPL", "MSFT", "GOOGL"]
            df = yf.download(tickers=tickers, period="5d", progress=False)
            if not df.empty:
                logger.info(f"✓ 成功批量获取")
                logger.info(f"  形状: {df.shape}")
            else:
                logger.warning("✗ 批量获取数据为空")
        except Exception as e:
            logger.error(f"✗ 批量获取失败: {e}")
        
    except ImportError as e:
        logger.error(f"✗ yFinance 导入失败: {e}")
        return False
    
    return True


def test_network():
    """测试网络连接"""
    logger.info("\n" + "=" * 60)
    logger.info("测试网络连接")
    logger.info("=" * 60)
    
    import urllib.request
    import ssl
    
    # 测试 1: 访问百度
    logger.info("\n[测试 1] 访问百度...")
    try:
        response = urllib.request.urlopen("https://www.baidu.com", timeout=10)
        logger.info(f"✓ 百度访问成功，状态码: {response.getcode()}")
    except Exception as e:
        logger.error(f"✗ 百度访问失败: {e}")
    
    # 测试 2: 访问 GitHub
    logger.info("\n[测试 2] 访问 GitHub...")
    try:
        response = urllib.request.urlopen("https://github.com", timeout=10)
        logger.info(f"✓ GitHub 访问成功，状态码: {response.getcode()}")
    except Exception as e:
        logger.error(f"✗ GitHub 访问失败: {e}")
    
    # 测试 3: 检查代理设置
    logger.info("\n[测试 3] 检查环境变量...")
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            logger.info(f"  {var} = {value}")
        else:
            logger.info(f"  {var} = (未设置)")


def main():
    logger.info("开始数据源诊断测试")
    logger.info("这个测试会检查各个数据源是否可用\n")
    
    # 测试网络
    test_network()
    
    # 测试 AKShare
    test_akshare()
    
    # 测试 yFinance
    test_yfinance()
    
    logger.info("\n" + "=" * 60)
    logger.info("测试完成")
    logger.info("=" * 60)
    
    logger.info("\n诊断建议:")
    logger.info("1. 如果网络连接失败，请检查网络设置和代理")
    logger.info("2. 如果 AKShare 失败，可能是网络问题或 API 限制")
    logger.info("3. 如果 yFinance 失败，可能是速率限制，请等待一段时间")
    logger.info("4. 如果都失败，可以使用模拟数据测试分析功能")


if __name__ == "__main__":
    main()
