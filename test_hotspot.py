"""
测试市场热点收集器
"""

import logging
from hotspot_collector import MarketHotspotCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_hotspot_collector():
    """测试热点收集器"""
    logger.info("=" * 60)
    logger.info("开始测试市场热点收集器")
    logger.info("=" * 60)
    logger.info("")
    
    # 创建收集器
    collector = MarketHotspotCollector()
    
    # 运行收集和分析
    result = collector.run()
    
    # 显示结果
    if result:
        logger.info("\n" + "=" * 60)
        logger.info("热点收集器测试完成")
        logger.info("=" * 60)
        logger.info(f"\n识别到 {len(result.get('hotspots', []))} 个热点板块:")
        
        for hotspot in result.get('hotspots', []):
            logger.info(f"  • {hotspot['sector']} (评分: {hotspot['score']:.1f})")
            logger.info(f"    关键词: {', '.join(hotspot['keywords'][:3])}")
    else:
        logger.warning("热点收集器未返回结果")


if __name__ == "__main__":
    test_hotspot_collector()
