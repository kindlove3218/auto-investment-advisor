"""
市场热点搜索器（简化版）

说明：由于网络代理限制，这个版本提供框架，可以配合 MCP websearch 使用
"""

import json
import logging
from datetime import datetime
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HotspotAnalyzer:
    def __init__(self):
        pass

    def analyze_search_results(self, search_results: List[Dict]) -> List[Dict]:
        """
        分析搜索结果，提取热点板块
        
        参数：
            search_results: 从 MCP websearch 或其他搜索服务获取的搜索结果
            每个结果应包含: {'title': str, 'content': str, 'url': str}
        """
        logger.info("分析搜索结果...")
        
        # 定义板块关键词
        sector_keywords = {
            '人工智能': ['AI', '人工智能', '大模型', 'ChatGPT', '算力'],
            '新能源': ['新能源', '光伏', '风电', '储能', '锂电', '充电桩'],
            '半导体': ['芯片', '半导体', '集成电路', '存储', '封测'],
            '医药': ['医药', '医疗', '疫苗', '创新药', '医疗器械'],
            '消费': ['消费', '白酒', '家电', '食品', '零售', '免税'],
            '金融': ['银行', '证券', '保险', '金融', '信托', '期货'],
            '地产': ['地产', '房地产', '物业管理', '基建', '建材'],
            '军工': ['军工', '航天', '卫星', '国防', '导弹'],
            '通信': ['通信', '5G', '6G', '基站', '光通信'],
            '汽车': ['汽车', '新能源车', '智能驾驶', '激光雷达'],
        }
        
        # 统计每个板块的热度
        hotspot_scores = {}
        
        for result in search_results:
            title = result.get('title', '')
            content = result.get('content', '')
            full_text = f"{title} {content}".lower()
            
            # 检查每个板块
            for sector, keywords in sector_keywords.items():
                match_count = sum(1 for keyword in keywords if keyword.lower() in full_text)
                
                if match_count > 0:
                    if sector not in hotspot_scores:
                        hotspot_scores[sector] = {
                            'sector': sector,
                            'score': 0,
                            'match_count': 0,
                            'related_news': []
                        }
                    
                    hotspot_scores[sector]['score'] += match_count * 10
                    hotspot_scores[sector]['match_count'] += match_count
                    
                    # 添加相关新闻
                    if len(hotspot_scores[sector]['related_news']) < 5:
                        hotspot_scores[sector]['related_news'].append({
                            'title': title,
                            'url': result.get('url', ''),
                            'snippet': content[:200]
                        })
        
        # 转换为列表并排序
        hotspots = list(hotspot_scores.values())
        hotspots.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"识别出 {len(hotspots)} 个热点板块")
        
        return hotspots[:10]

    def format_text_report(self, hotspots: List[Dict]) -> str:
        """生成文本报告"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"                    市场热点分析报告")
        lines.append(f"              {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        lines.append("=" * 80)
        lines.append("")
        
        for idx, hotspot in enumerate(hotspots, 1):
            lines.append(f"【{idx}】{hotspot['sector']}")
            lines.append(f"    热度评分: {hotspot['score']:.1f}")
            lines.append(f"    匹配次数: {hotspot['match_count']}")
            
            if hotspot.get('related_news'):
                lines.append(f"    相关新闻 ({len(hotspot['related_news'])} 条):")
                for news in hotspot['related_news'][:3]:
                    lines.append(f"      • {news['title'][:80]}")
                    lines.append(f"        {news['url']}")
            
            lines.append("")
        
        lines.append("=" * 80)
        lines.append("使用说明：")
        lines.append("1. 使用 MCP websearch 搜索以下关键词：")
        lines.append("   'A股 市场热点 最新'、'股市 题材概念'、'热点板块'")
        lines.append("")
        lines.append("2. 将搜索结果传入 analyze_search_results() 方法")
        lines.append("")
        lines.append("3. 查看生成的热点分析报告")
        lines.append("")
        lines.append("示例：")
        lines.append("  search_results = [")
        lines.append("      {'title': '人工智能板块持续走强', 'content': '...', 'url': '...'},")
        lines.append("      {'title': '新能源政策利好', 'content': '...', 'url': '...'}")
        lines.append("  ]")
        lines.append("  analyzer = HotspotAnalyzer()")
        lines.append("  hotspots = analyzer.analyze_search_results(search_results)")
        lines.append("  report = analyzer.format_text_report(hotspots)")
        lines.append("  print(report)")
        lines.append("=" * 80)
        
        return '\n'.join(lines)

    def save_results(self, hotspots: List[Dict], report: str):
        """保存结果"""
        import os
        
        os.makedirs('data', exist_ok=True)
        
        # 保存 JSON
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = f"data/hotspots_{timestamp}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'hotspots': hotspots
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"热点数据已保存: {json_file}")
        
        # 保存报告
        txt_file = f"data/hotspots_report_{timestamp}.txt"
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"分析报告已保存: {txt_file}")


if __name__ == "__main__":
    # 示例：如何使用
    logger.info("市场热点搜索器 - 使用示例")
    logger.info("")
    logger.info("方法 1: 结合 MCP websearch")
    logger.info("  1. 使用 MCP websearch 搜索市场热点")
    logger.info("  2. 获取搜索结果")
    logger.info("  3. 传入 analyzer.analyze_search_results()")
    logger.info("")
    logger.info("方法 2: 直接使用搜索结果")
    logger.info("  参考下面的示例代码")
    logger.info("")
    
    # 示例搜索结果
    sample_search_results = [
        {
            'title': '人工智能板块持续走强，多只个股涨停',
            'content': '受利好消息影响，人工智能板块今日表现强劲，多只个股涨停。大模型、算力等细分领域表现突出。',
            'url': 'https://example.com/news/1'
        },
        {
            'title': '新能源政策利好，光伏板块大涨',
            'content': '国家出台新能源支持政策，光伏、风电等板块应声大涨。储能、锂电池等产业链全线飘红。',
            'url': 'https://example.com/news/2'
        },
        {
            'title': '半导体板块活跃，国产替代加速',
            'content': '半导体板块今日活跃，国产替代加速推进。芯片、设备等细分领域表现优异。',
            'url': 'https://example.com/news/3'
        }
    ]
    
    # 创建分析器
    analyzer = HotspotAnalyzer()
    
    # 分析
    hotspots = analyzer.analyze_search_results(sample_search_results)
    
    # 生成报告
    report = analyzer.format_text_report(hotspots)
    
    # 保存
    analyzer.save_results(hotspots, report)
    
    # 显示报告
    print("\n" + report)
