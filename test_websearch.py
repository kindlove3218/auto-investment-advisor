"""
测试 MCP websearch 功能
"""

import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSearchTester:
    def __init__(self):
        pass

    def test_search_query(self, query: str) -> bool:
        """
        测试搜索功能
        
        注意：这个脚本需要 MCP websearch 服务可用
        如果 MCP 服务不可用，请使用手动搜索结果
        """
        logger.info("=" * 60)
        logger.info(f"测试搜索查询: {query}")
        logger.info("=" * 60)
        logger.info("")
        
        # 检查 MCP 配置
        logger.info("[步骤 1/3] 检查 MCP 配置...")
        try:
            mcp_config_path = '/Users/qulong/.config/opencode/mcp_config.json'
            
            with open(mcp_config_path, 'r') as f:
                mcp_config = json.load(f)
            
            logger.info(f"  ✓ MCP 配置文件存在")
            logger.info(f"  配置的服务器: {list(mcp_config.get('mcpServers', {}).keys())}")
            
            # 检查 Tavily
            if 'tavily' in mcp_config.get('mcpServers', {}):
                logger.info(f"  • Tavily: ✓ 已配置")
            else:
                logger.warning(f"  • Tavily: ✗ 未配置")
            
            # 检查 open-websearch
            if 'open-websearch' in mcp_config.get('mcpServers', {}):
                logger.info(f"  • open-websearch: ✓ 已配置")
                logger.info(f"      搜索引擎: {mcp_config['mcpServers']['open-websearch'].get('args', [])}")
            else:
                logger.warning(f"  • open-websearch: ✗ 未配置")
            
        except Exception as e:
            logger.error(f"  ✗ 读取 MCP 配置失败: {e}")
            return False
        
        logger.info("")
        
        # 尝试搜索（这里需要实际的 MCP websearch 调用）
        logger.info("[步骤 2/3] 测试搜索功能...")
        logger.info(f"  查询: {query}")
        logger.info("")
        logger.info("  注意：")
        logger.info("  如果 MCP websearch 在当前环境中可用，")
        logger.info("  可以直接调用搜索功能。")
        logger.info("  如果不可用，请手动搜索并输入结果。")
        logger.info("")
        
        # 由于我们在这个环境中无法直接调用 MCP websearch，
        # 我们提供一个手动输入的方式
        logger.info("[步骤 3/3] 手动输入搜索结果（或使用 MCP websearch）")
        logger.info("")
        logger.info("选项 1: 如果 MCP websearch 可用，直接使用")
        logger.info("  可以在支持 MCP 的环境中运行:")
        logger.info(f"  websearch '{query}'")
        logger.info("")
        logger.info("选项 2: 手动搜索并输入结果")
        logger.info("  在浏览器中搜索:")
        logger.info(f"  - 百度: https://www.baidu.com/s?wd={query}")
        logger.info(f"  - 谷歌: https://www.google.com/search?q={query}")
        logger.info("  然后复制新闻标题和链接到下面")
        logger.info("")
        
        # 提供输入界面
        try:
            print("请输入搜索结果（格式：标题|链接，一行一个，输入 'done' 结束）:")
            print("示例:")
            print("  人工智能板块持续走强|https://example.com/news/1")
            print("  新能源政策利好|https://example.com/news/2")
            print("  done")
            print("")
            
            search_results = []
            
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
            
            if search_results:
                logger.info(f"\n  ✓ 收集到 {len(search_results)} 条搜索结果")
                return search_results
            else:
                logger.warning("  ✗ 未输入任何结果")
                return []
        
        except KeyboardInterrupt:
            logger.info("\n  用户中断")
            return []
        except Exception as e:
            logger.error(f"  ✗ 输入失败: {e}")
            return []

    def test_market_hotspot_search(self):
        """测试市场热点搜索"""
        queries = [
            "A股 市场热点 最新",
            "股市 题材概念",
            "热点板块",
            "主线题材",
            "市场风口"
        ]
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("测试市场热点搜索")
        logger.info("=" * 60)
        logger.info("")
        
        for idx, query in enumerate(queries, 1):
            logger.info(f"[{idx}/{len(queries)}] 搜索: {query}")
            
            results = self.test_search_query(query)
            
            if results:
                logger.info(f"  ✓ 获取到 {len(results)} 条结果")
            else:
                logger.warning(f"  ✗ 未获取到结果")
            
            logger.info("")
            
            # 延时，避免搜索过快
            if idx < len(queries):
                logger.info("等待 2 秒...")
                import time
                time.sleep(2)

    def save_search_results(self, query: str, results: list, filename: str = None):
        """保存搜索结果"""
        import os
        
        os.makedirs('data', exist_ok=True)
        
        if not filename:
            filename = f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join('data', filename)
        
        data = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'count': len(results)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"搜索结果已保存: {filepath}")
        return filepath


def main():
    """主函数"""
    import sys
    
    logger.info("=" * 60)
    logger.info("MCP WebSearch 功能测试")
    logger.info("=" * 60)
    logger.info("")
    
    # 创建测试器
    tester = WebSearchTester()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == 'test':
            # 测试单个查询
            if len(sys.argv) > 2:
                query = ' '.join(sys.argv[2:])
                results = tester.test_search_query(query)
                
                if results:
                    tester.save_search_results(query, results)
        elif mode == 'hotspot':
            # 测试市场热点搜索
            tester.test_market_hotspot_search()
        else:
            logger.error(f"未知模式: {mode}")
            logger.info("可用模式: test <query>, hotspot")
    else:
        # 显示使用说明
        logger.info("使用方法:")
        logger.info("")
        logger.info("1. 测试单个查询:")
        logger.info("   python test_websearch.py test 'A股 市场热点 最新'")
        logger.info("")
        logger.info("2. 测试市场热点搜索:")
        logger.info("   python test_websearch.py hotspot")
        logger.info("")
        logger.info("说明:")
        logger.info("- 如果 MCP websearch 可用，可以直接使用")
        logger.info("- 如果不可用，会提示手动输入搜索结果")
        logger.info("- 搜索结果会保存到 data/search_results_*.json")
        logger.info("")
        
        logger.info("=" * 60)
        logger.info("准备测试？运行以上命令")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
