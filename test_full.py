"""
完整测试流程 - 使用模拟数据
"""

import os
import sys
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_full_flow():
    """测试完整流程"""
    logger.info("=" * 60)
    logger.info("开始完整测试流程")
    logger.info("=" * 60)
    
    # 步骤 1: 生成模拟数据
    logger.info("\n[步骤 1/4] 生成模拟数据")
    os.system('python generate_mock_data.py')
    
    # 获取最新生成的数据文件
    import glob
    data_files = glob.glob('data/market_data_*.json')
    if not data_files:
        logger.error("未找到数据文件")
        return False
    
    latest_data_file = max(data_files, key=os.path.getctime)
    logger.info(f"使用数据文件: {latest_data_file}")
    
    # 步骤 2: 分析股票
    logger.info("\n[步骤 2/4] 分析股票")
    os.system(f'python analyze_stocks.py {latest_data_file}')
    
    # 步骤 3: 查看生成的报告
    logger.info("\n[步骤 3/4] 查看报告")
    import glob
    report_files = glob.glob('reports/report_*.html')
    if report_files:
        latest_report = max(report_files, key=os.path.getctime)
        logger.info(f"报告已生成: {latest_report}")
        os.system(f'open {latest_report}')
    
    # 步骤 4: 测试单独模块
    logger.info("\n[步骤 4/4] 测试单独模块")
    
    logger.info("\n测试 1: 只运行数据获取模式")
    os.system('export RUN_MODE=fetch && python main.py')
    
    logger.info("\n测试 2: 只运行股票分析模式")
    os.system('export RUN_MODE=analyze && python main.py')
    
    logger.info("\n" + "=" * 60)
    logger.info("测试完成！")
    logger.info("=" * 60)
    
    return True


if __name__ == "__main__":
    test_full_flow()
