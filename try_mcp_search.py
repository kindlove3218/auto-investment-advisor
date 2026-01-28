"""
尝试使用 MCP websearch 搜索市场热点

注意：这个脚本需要在支持 MCP websearch 的环境中运行
"""

import json
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_mcp_websearch():
    """测试 MCP websearch 是否可用"""
    logger.info("=" * 60)
    logger.info("测试 MCP websearch")
    logger.info("=" * 60)
    logger.info("")
    
    # 测试查询
    test_queries = [
        "A股 市场热点 最新",
        "股市 题材概念"
    ]
    
    for query in test_queries:
        logger.info(f"测试查询: {query}")
        
        try:
            # 尝试调用 websearch 命令
            result = subprocess.run(
                ['websearch', query],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info(f"  ✓ websearch 可用")
                logger.info(f"  输出预览: {result.stdout[:200]}...")
                return True
            else:
                logger.error(f"  ✗ websearch 不可用")
                logger.error(f"  错误: {result.stderr}")
        
        except subprocess.TimeoutExpired:
            logger.error(f"  ✗ 超时")
        except FileNotFoundError:
            logger.error(f"  ✗ websearch 命令未找到")
        except Exception as e:
            logger.error(f"  ✗ 错误: {e}")
        
        logger.info("")
    
    logger.info("=" * 60)
    logger.info("测试完成")
    logger.info("=" * 60)
    logger.info("")
    
    return False


def use_manual_search():
    """使用手动搜索结果"""
    logger.info("=" * 60)
    logger.info("使用手动搜索结果")
    logger.info("=" * 60)
    logger.info("")
    
    logger.info("步骤 1: 在浏览器中搜索")
    logger.info("  请访问以下链接搜索：")
    logger.info("  • 百度: https://www.baidu.com/s?wd=A股 市场热点 最新")
    logger.info("  • 谷歌: https://www.google.com/search?q=A股 市场热点 最新")
    logger.info("")
    
    logger.info("步骤 2: 复制搜索结果")
    logger.info("  从搜索结果中选择 5-10 条新闻")
    logger.info("  复制标题和链接")
    logger.info("")
    
    logger.info("步骤 3: 创建搜索结果文件")
    logger.info("  创建文件: search_results.json")
    logger.info("  格式:")
    logger.info("""  {
    "query": "A股 市场热点 最新",
    "results": [
      {
        "title": "新闻标题",
        "content": "内容摘要",
        "url": "新闻链接"
      }
    ]
  }""")
    logger.info("")
    
    logger.info("步骤 4: 运行热点分析")
    logger.info("  运行: python search_analyze.py manual")
    logger.info("  然后粘贴搜索结果")
    logger.info("")
    
    logger.info("=" * 60)
    logger.info("等待手动搜索...")
    logger.info("=" * 60)


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("市场热点收集器 - 真实搜索测试")
    logger.info("=" * 60)
    logger.info("")
    
    # 先测试 MCP websearch
    mcp_available = test_mcp_websearch()
    
    if not mcp_available:
        logger.info("MCP websearch 不可用，切换到手动模式...")
        logger.info("")
        
        import time
        time.sleep(2)
        
        use_manual_search()


if __name__ == "__main__":
    main()
