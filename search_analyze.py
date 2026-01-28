"""
市场热点搜索与分析 - 完整集成脚本

支持：
1. 使用 MCP websearch 搜索（如果可用）
2. 手动输入搜索结果
3. 自动分析热点板块
4. 生成文本报告
"""

import json
import logging
from datetime import datetime
from hotspot_analyzer import HotspotAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketHotspotManager:
    def __init__(self):
        self.analyzer = HotspotAnalyzer()
        self.search_queries = [
            "A股 市场热点 最新",
            "股市 题材概念",
            "热点板块",
            "主线题材",
            "市场风口",
            "政策利好 板块",
            "涨停板 热点"
        ]

    def manual_input_results(self) -> list:
        """手动输入搜索结果"""
        logger.info("=" * 60)
        logger.info("手动输入搜索结果")
        logger.info("=" * 60)
        logger.info("")
        
        logger.info("请在浏览器中搜索以下查询之一：")
        for idx, query in enumerate(self.search_queries, 1):
            logger.info(f"  {idx}. {query}")
        
        logger.info("")
        logger.info("然后输入搜索结果（格式：标题|链接）")
        logger.info("一行一个，输入 'done' 结束")
        logger.info("")
        
        search_results = []
        
        try:
            while True:
                user_input = input("> ").strip()
                
                if user_input.lower() == 'done':
                    break
                
                if user_input:
                    parts = user_input.split('|', 1)
                    if len(parts) == 2:
                        search_results.append({
                            'title': parts[0].strip(),
                            'url': parts[1].strip(),
                            'content': ''
                        })
                    else:
                        # 只有标题
                        search_results.append({
                            'title': user_input,
                            'url': '',
                            'content': ''
                        })
            
            logger.info(f"✓ 收集到 {len(search_results)} 条搜索结果")
            return search_results
        
        except KeyboardInterrupt:
            logger.info("\n用户中断")
            return []
        except Exception as e:
            logger.error(f"输入失败: {e}")
            return []

    def use_mcp_websearch_results(self, query: str) -> list:
        """
        使用 MCP websearch 搜索
        
        注意：这个方法需要 MCP websearch 服务可用
        在支持 MCP 的环境中，可以直接调用 websearch 工具
        """
        logger.info("=" * 60)
        logger.info(f"使用 MCP websearch 搜索")
        logger.info("=" * 60)
        logger.info("")
        logger.info(f"查询: {query}")
        logger.info("")
        
        # 由于我们在这个环境中无法直接调用 MCP websearch，
        # 这里提供一个说明和使用示例
        
        logger.info("MCP websearch 使用说明：")
        logger.info("")
        logger.info("在支持 MCP 的环境中（如 opencode），可以运行：")
        logger.info(f"  websearch '{query}'")
        logger.info("")
        logger.info("然后将搜索结果整理为以下格式：")
        logger.info("  [")
        logger.info("      {")
        logger.info("        'title': '新闻标题',")
        logger.info("        'content': '内容摘要',")
        logger.info("        'url': '新闻链接'")
        logger.log("      },")
        logger.info("      ...")
        logger.log("  ]")
        logger.info("")
        logger.info("然后传入 analyze_search_results() 方法")
        logger.info("")
        
        # 返回空列表，等待用户手动输入
        return []

    def create_sample_results(self) -> list:
        """创建示例搜索结果"""
        logger.info("=" * 60)
        logger.info("使用示例搜索结果（用于测试）")
        logger.info("=" * 60)
        logger.info("")
        
        return [
            {
                'title': '人工智能板块持续走强，多只个股涨停',
                'content': '受利好消息影响，人工智能板块今日表现强劲，多只个股涨停。大模型、算力等细分领域表现突出。',
                'url': 'https://finance.example.com/news/1'
            },
            {
                'title': '新能源政策利好，光伏板块大涨',
                'content': '国家出台新能源支持政策，光伏、风电等板块应声大涨。储能、锂电池等产业链全线飘红。',
                'url': 'https://finance.example.com/news/2'
            },
            {
                'title': '半导体板块活跃，国产替代加速',
                'content': '半导体板块今日活跃，国产替代加速推进。芯片、设备等细分领域表现优异。',
                'url': 'https://finance.example.com/news/3'
            },
            {
                'title': '医药板块反弹，创新药表现亮眼',
                'content': '医药板块今日出现反弹，创新药表现亮眼。医疗器械、疫苗等细分领域均有上涨。',
                'url': 'https://finance.example.com/news/4'
            },
            {
                'title': '消费板块回暖，白酒家电领涨',
                'content': '消费板块今日回暖，白酒、家电领涨。免税、零售等细分领域跟随上涨。',
                'url': 'https://finance.example.com/news/5'
            },
            {
                'title': '军工板块活跃，卫星导航概念走强',
                'content': '军工板块今日活跃，卫星导航概念走强。航天、国防等细分领域表现优异。',
                'url': 'https://finance.example.com/news/6'
            },
            {
                'title': '通信板块上涨，5G 概念表现强势',
                'content': '通信板块今日上涨，5G 概念表现强势。基站、光通信等细分领域均有涨幅。',
                'url': 'https://finance.example.com/news/7'
            },
            {
                'title': '金融板块稳定，银行保险小幅上涨',
                'content': '金融板块今日表现稳定，银行、保险小幅上涨。证券、信托等细分领域持平。',
                'url': 'https://finance.example.com/news/8'
            },
            {
                'title': '汽车板块活跃，新能源车概念走强',
                'content': '汽车板块今日活跃，新能源车概念走强。智能驾驶、激光雷达等细分领域表现突出。',
                'url': 'https://finance.example.com/news/9'
            },
            {
                'title': '有色板块上涨，铜铝价格反弹',
                'content': '有色板块今日上涨，铜铝价格反弹。黄金、白银等贵金属也有涨幅。',
                'url': 'https://finance.example.com/news/10'
            }
        ]

    def analyze_hotspots(self, search_results: list) -> dict:
        """分析热点板块"""
        logger.info("=" * 60)
        logger.info("分析市场热点")
        logger.info("=" * 60)
        logger.info("")
        
        # 使用热点分析器
        hotspots = self.analyzer.analyze_search_results(search_results)
        
        # 生成报告
        report = self.analyzer.format_text_report(hotspots)
        
        # 保存结果
        self.analyzer.save_results(hotspots, report)
        
        return {
            'search_results': search_results,
            'hotspots': hotspots,
            'report': report
        }

    def run(self, mode: str = 'manual'):
        """执行完整流程"""
        logger.info("=" * 60)
        logger.info("市场热点搜索与分析系统")
        logger.info(f"运行时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        logger.info("=" * 60)
        logger.info("")
        
        # 步骤 1: 搜索
        search_results = []
        
        if mode == 'mcp':
            # 使用 MCP websearch
            query = self.search_queries[0]
            search_results = self.use_mcp_websearch_results(query)
            
            if not search_results:
                # MCP websearch 不可用，切换到手动输入
                logger.info("切换到手动输入模式...")
                search_results = self.manual_input_results()
        
        elif mode == 'sample':
            # 使用示例数据
            search_results = self.create_sample_results()
        
        else:
            # 默认：手动输入
            search_results = self.manual_input_results()
        
        # 步骤 2: 分析
        if search_results:
            result = self.analyze_hotspots(search_results)
            
            # 步骤 3: 显示报告
            logger.info("\n" + result['report'])
            
            logger.info("\n" + "=" * 60)
            logger.info("流程完成！")
            logger.info("=" * 60)
            logger.info("")
            logger.info("数据文件:")
            logger.info("  • JSON: data/hotspots_*.json")
            logger.info("  • 报告: data/hotspots_report_*.txt")
            logger.info("")
        else:
            logger.warning("未获取到搜索结果，无法分析")


def main():
    """主函数"""
    import sys
    
    logger.info("=" * 60)
    logger.info("市场热点搜索与分析系统")
    logger.info("=" * 60)
    logger.info("")
    
    # 显示使用说明
    logger.info("使用方法:")
    logger.info("")
    logger.info("1. 手动输入搜索结果:")
    logger.info("   python search_analyze.py manual")
    logger.info("")
    logger.info("2. 使用示例数据（测试）:")
    logger.info("   python search_analyze.py sample")
    logger.info("")
    logger.info("3. 使用 MCP websearch:")
    logger.info("   python search_analyze.py mcp")
    logger.info("")
    logger.info("说明:")
    logger.info("- manual: 手动输入搜索结果")
    logger.info("- sample: 使用内置的示例数据")
    logger.info("- mcp: 尝试使用 MCP websearch（需要在支持 MCP 的环境）")
    logger.info("")
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        manager = MarketHotspotManager()
        
        if mode in ['manual', 'mcp', 'sample']:
            manager.run(mode)
        else:
            logger.error(f"未知模式: {mode}")
            logger.info("可用模式: manual, mcp, sample")
            sys.exit(1)
    else:
        # 默认运行示例
        logger.info("未指定模式，使用示例数据运行...")
        logger.info("")
        
        import time
        time.sleep(2)
        
        manager = MarketHotspotManager()
        manager.run('sample')


if __name__ == "__main__":
    main()
