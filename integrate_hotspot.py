"""
整合测试：市场热点收集器
"""

import json
import logging
from hotspot_analyzer import HotspotAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_with_sample_data():
    """使用示例数据测试热点分析器"""
    logger.info("=" * 60)
    logger.info("测试热点分析器（使用示例数据）")
    logger.info("=" * 60)
    
    # 创建分析器
    analyzer = HotspotAnalyzer()
    
    # 使用示例数据
    sample_search_results = [
        {
            'title': '人工智能板块持续走强，多只个股涨停',
            'content': '受利好消息影响，人工智能板块今日表现强劲，多只个股涨停。大模型、算力等细分领域表现突出。ChatGPT概念股全线飘红。',
            'url': 'https://example.com/news/ai'
        },
        {
            'title': '新能源政策利好，光伏板块大涨',
            'content': '国家出台新能源支持政策，光伏、风电等板块应声大涨。储能、锂电池等产业链全线飘红。光伏龙头股涨停。',
            'url': 'https://example.com/news/new-energy'
        },
        {
            'title': '半导体板块活跃，国产替代加速',
            'content': '半导体板块今日活跃，国产替代加速推进。芯片、设备等细分领域表现优异。存储芯片概念股表现强势。',
            'url': 'https://example.com/news/semiconductor'
        },
        {
            'title': '医药板块反弹，创新药表现亮眼',
            'content': '医药板块今日出现反弹，创新药表现亮眼。医疗器械、疫苗等细分领域均有上涨。医药龙头股资金净流入。',
            'url': 'https://example.com/news/medicine'
        },
        {
            'title': '消费板块回暖，白酒家电领涨',
            'content': '消费板块今日回暖，白酒、家电领涨。免税、零售等细分领域跟随上涨。消费龙头股表现稳健。',
            'url': 'https://example.com/news/consumer'
        },
        {
            'title': '金融板块稳定，银行保险小幅上涨',
            'content': '金融板块今日表现稳定，银行、保险小幅上涨。证券、信托等细分领域持平。金融板块估值处于历史低位。',
            'url': 'https://example.com/news/finance'
        },
        {
            'title': '军工板块活跃，卫星导航概念走强',
            'content': '军工板块今日活跃，卫星导航概念走强。航天、国防等细分领域表现优异。军工龙头股成交量放大。',
            'url': 'https://example.com/news/military'
        }
    ]
    
    # 分析热点
    hotspots = analyzer.analyze_search_results(sample_search_results)
    
    # 生成报告
    report = analyzer.format_text_report(hotspots)
    
    # 保存结果
    analyzer.save_results(hotspots, report)
    
    # 显示结果摘要
    logger.info("\n" + "=" * 60)
    logger.info("热点分析结果摘要")
    logger.info("=" * 60)
    
    for idx, hotspot in enumerate(hotspots, 1):
        logger.info(f"{idx}. {hotspot['sector']}")
        logger.info(f"   评分: {hotspot['score']:.1f}")
        logger.info(f"   匹配: {hotspot['match_count']} 次")
        logger.info(f"   新闻: {len(hotspot.get('related_news', []))} 条")
    
    logger.info("\n详细报告:")
    logger.info(report)
    
    return hotspots


def test_with_mcp_websearch():
    """测试如何与 MCP websearch 集成"""
    logger.info("=" * 60)
    logger.info("热点分析器与 MCP websearch 集成示例")
    logger.info("=" * 60)
    logger.info("")
    
    logger.info("步骤 1：使用 MCP websearch 搜索市场热点")
    logger.info("  搜索关键词：")
    logger.info("    - 'A股 市场热点 最新'")
    logger.info("    - '股市 题材概念'")
    logger.info("    - '热点板块'")
    logger.info("")
    
    logger.info("步骤 2：获取搜索结果")
    logger.info("  将搜索结果整理为以下格式：")
    logger.info("  [")
    logger.info("      {")
    logger.info("        'title': '新闻标题',")
    logger.info("        'content': '新闻内容摘要',")
    logger.info("        'url': '新闻链接'")
    logger.info("      },")
    logger.info("      ...")
    logger.info("  ]")
    logger.info("")
    
    logger.info("步骤 3：运行热点分析")
    logger.info("  Python 代码：")
    logger.info("  ```python")
    logger.info("  from hotspot_analyzer import HotspotAnalyzer")
    logger.info("  ")
    logger.info("  # 1. 加载搜索结果（可以来自 MCP websearch）")
    logger.info("  with open('search_results.json', 'r') as f:")
    logger.info("      search_results = json.load(f)")
    logger.info("  ")
    logger.info("  # 2. 分析热点")
    logger.info("  analyzer = HotspotAnalyzer()")
    logger.info("  hotspots = analyzer.analyze_search_results(search_results)")
    logger.info("  ")
    logger.info("  # 3. 生成报告")
    logger.info("  report = analyzer.format_text_report(hotspots)")
    logger.info("  ")
    logger.info("  # 4. 保存结果")
    logger.info("  analyzer.save_results(hotspots, report)")
    logger.info("  ")
    logger.info("  # 5. 显示报告")
    logger.info("  print(report)")
    logger.info("  ```")
    logger.info("")
    
    logger.info("步骤 4：查看生成的报告")
    logger.info("  报告文件：data/hotspots_report_*.txt")
    logger.info("  JSON 数据：data/hotspots_*.json")
    logger.info("")
    
    logger.info("=" * 60)
    logger.info("集成说明完成")
    logger.info("=" * 60)


def show_usage_flow():
    """显示完整使用流程"""
    logger.info("\n" + "=" * 60)
    logger.info("市场热点收集器 - 完整使用流程")
    logger.info("=" * 60)
    logger.info("")
    
    logger.info("方式 1：独立使用（推荐）")
    logger.info("  1. 使用 MCP websearch 搜索市场热点")
    logger.info("  2. 整理搜索结果为 JSON 格式")
    logger.info("  3. 运行：python hotspot_analyzer.py")
    logger.info("  4. 查看生成的热点报告")
    logger.info("")
    
    logger.info("方式 2：集成到主程序")
    logger.info("  1. 在 main.py 中添加热点收集步骤")
    logger.info("  2. 使用热点筛选股票")
    logger.info("  3. 将热点板块信息加入投资报告")
    logger.info("")
    
    logger.info("方式 3：定时任务")
    logger.info("  1. 配置 GitHub Actions 定时任务")
    logger.info("  2. 先运行热点收集")
    logger.info("  3. 再运行股票分析")
    logger.info("  4. 发送包含热点信息的投资报告")
    logger.info("")
    
    logger.info("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == 'sample':
            test_with_sample_data()
        elif mode == 'mcp':
            test_with_mcp_websearch()
        elif mode == 'flow':
            show_usage_flow()
        else:
            logger.error(f"未知模式: {mode}")
            logger.info("可用模式: sample, mcp, flow")
    else:
        # 默认运行示例
        test_with_sample_data()
        
        # 显示使用流程
        show_usage_flow()
