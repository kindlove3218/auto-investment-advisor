"""
市场热点提取器 - 优化版

从搜索结果中智能提取热点板块，避免重复和错误识别
"""

import json
import logging
import re
from datetime import datetime
from typing import Dict, List
from collections import Counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OptimizedHotspotExtractor:
    def __init__(self):
        # 定义板块关键词（用于匹配和过滤）
        self.sector_keywords = {
            '人工智能': ['AI', '人工智能', '大模型', 'ChatGPT', '算力', '机器学习', '深度学习'],
            '新能源': ['新能源', '光伏', '风电', '储能', '锂电', '充电桩', '新能源车', '氢能'],
            '半导体': ['芯片', '半导体', '集成电路', '存储', '封测', '晶圆'],
            '医药': ['医药', '医疗', '疫苗', '创新药', '医疗器械', '生物制药'],
            '消费': ['消费', '白酒', '家电', '食品', '零售', '免税', '乳业', '啤酒'],
            '金融': ['银行', '证券', '保险', '金融', '信托', '期货', '券商', '资管'],
            '地产': ['地产', '房地产', '物业管理', '基建', '建材', '水泥', '钢铁'],
            '军工': ['军工', '航天', '卫星', '国防', '导弹', '航空', '航天器'],
            '通信': ['通信', '5G', '6G', '基站', '光通信', '光纤', '通信设备'],
            '汽车': ['汽车', '新能源车', '智能驾驶', '激光雷达', '车联网', '自动驾驶'],
            '有色': ['有色', '铜', '铝', '黄金', '白银', '贵金属', '稀土'],
        }
        
        # 从新闻标题提取板块的模式（更精确）
        self.sector_patterns = [
            # 匹配"XX板块"或"XX概念"
            r'([^\uff00-\ufffff]+?板块|概念)',
            
            # 匹配"XX题材"、"XX主线"
            r'([^\uff00-\ufffff]+?题材|主线)',
            
            # 匹配特定词汇
            r'([^\uff00-\ufffff]{2,6}?板块?指数|龙头)',
            
            # 匹配特定的热门术语
            r'([^、，。\s]{2,6}?热点|风口)',
        ]
        
        # 板块权重（重要程度）
        self.sector_weights = {
            '人工智能': 1.5,
            '新能源': 1.5,
            '半导体': 1.3,
            '医药': 1.2,
            '金融': 1.2,
            '消费': 1.1,
            '军工': 1.3,
            '通信': 1.1,
            '汽车': 1.1,
            '地产': 1.0,
            '有色': 1.0,
        }
        
        # 定义一些应该忽略的词
        self.ignore_words = {
            '政策', '利好', '消息', '上涨', '下跌', '涨停', '跌停',
            '今日', '昨日', '本周', '本月', 'A股', '股市',
            '投资', '交易', '买卖', '持有', '建议', '风险',
            '最新', '相关', '板块', '概念', '题材', '主线'
        }
    
    def extract_sector_from_text(self, text: str) -> str:
        """从文本中提取单个板块名称"""
        sectors = []
        
        # 方法 1: 使用关键词匹配
        for sector, keywords in self.sector_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    sectors.append(sector)
                    break
        
        # 方法 2: 使用正则提取
        for pattern in self.sector_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple) and len(match) > 1:
                    sector_name = match[1].strip()
                    # 过滤掉应该忽略的词
                    if (len(sector_name) >= 2 and 
                        sector_name not in self.ignore_words and
                        not any(ignore_word in sector_name for ignore_word in self.ignore_words)):
                        sectors.append(sector_name)
        
        # 选择最合理的提取结果
        if sectors:
            # 优先使用关键词匹配的结果
            return sectors[0]
        
        return ""
    
    def normalize_sector(self, sector: str) -> str:
        """规范化板块名称"""
        sector = sector.strip()
        
        # 移除后缀
        sector = re.sub(r'[板块|概念|题材|主线|指数|龙头]$', '', sector)
        
        # 使用关键词映射规范化
        for key, keywords in self.sector_keywords.items():
            for keyword in keywords:
                if keyword in sector:
                    return key
        
        return sector
    
    def extract_sectors_from_results(self, search_results: List[Dict]) -> Dict[str, List]:
        """从搜索结果中提取所有板块并统计"""
        sector_news = {}
        
        for result in search_results:
            title = result.get('title', '')
            content = result.get('content', '')
            url = result.get('url', '')
            
            # 合并标题和内容
            full_text = f"{title} {content}"
            
            # 提取板块
            sector = self.extract_sector_from_text(full_text)
            
            if sector:
                # 规范化
                sector = self.normalize_sector(sector)
                
                # 如果不是常见板块，尝试更精确的匹配
                if sector not in self.sector_keywords:
                    # 尝试从标题中直接提取
                    if '板块' in title or '概念' in title:
                        # 使用正则更精确地提取
                        pattern = r'([^\uff00-\ufffff]{2,8})[板块|概念]'
                        matches = re.findall(pattern, title)
                        if matches:
                            potential_sector = self.normalize_sector(matches[0])
                            if potential_sector in self.sector_keywords:
                                sector = potential_sector
                
                # 添加到对应的新闻列表
                if sector:
                    if sector not in sector_news:
                        sector_news[sector] = []
                    
                    # 检查是否已存在
                    existing_titles = [n.get('title', '') for n in sector_news[sector]]
                    
                    if title not in existing_titles:
                        sector_news[sector].append({
                            'title': title,
                            'content': content,
                            'url': url
                        })
        
        return sector_news
    
    def calculate_hotspot_scores(self, sector_news: Dict[str, List]) -> List[Dict]:
        """计算热点评分"""
        hotspots = []
        
        for sector, news_list in sector_news.items():
            news_count = len(news_list)
            
            if news_count == 0:
                continue
            
            # 1. 新闻数量分数 (50%)
            # 最多 100 分，每条新闻 5 分
            news_score = min(100, news_count * 5)
            
            # 2. 板块权重分数 (30%)
            # 根据板块重要性给基础分
            weight = self.sector_weights.get(sector, 1.0)
            weight_score = weight * 30
            
            # 3. 标题质量分数 (20%)
            # 检查标题中是否包含明确的板块关键词
            title_quality_score = 20  # 基础分
            for news in news_list:
                title = news.get('title', '')
                if sector in title:
                    title_quality_score = 30
                    break
            
            # 综合评分
            total_score = news_score * 0.5 + weight_score * 0.3 + title_quality_score * 0.2
            
            # 挑选代表性新闻
            representative_news = []
            for news in news_list[:3]:
                # 只保留必要字段
                representative_news.append({
                    'title': news.get('title', ''),
                    'url': news.get('url', '')
                })
            
            hotspots.append({
                'sector': sector,
                'score': round(total_score, 1),
                'news_count': news_count,
                'sector_weight': weight,
                'related_news': representative_news
            })
        
        # 按评分排序
        hotspots.sort(key=lambda x: x['score'], reverse=True)
        
        return hotspots[:10]
    
    def format_text_report(self, hotspots: List[Dict]) -> str:
        """生成文本报告"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"                    市场热点分析报告")
        lines.append(f"              {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"分析方法：")
        lines.append("1. 搜索市场热点关键词")
        lines.append("2. 从搜索结果中智能提取板块")
        lines.append("3. 按新闻数量和板块权重评分")
        lines.append("")
        
        for idx, hotspot in enumerate(hotspots, 1):
            lines.append(f"【{idx}】{hotspot['sector']}")
            lines.append(f"    热度评分: {hotspot['score']:.1f}")
            lines.append(f"    相关新闻: {hotspot['news_count']} 条")
            lines.append(f"    板块权重: {hotspot['sector_weight']}")
            
            if hotspot.get('related_news'):
                lines.append(f"    代表性新闻 ({min(3, len(hotspot['related_news']))} 条):")
                for news in hotspot['related_news']:
                    lines.append(f"      • {news['title'][:80]}")
            
            lines.append("")
        
        lines.append("=" * 80)
        lines.append("评分说明：")
        lines.append("• 新闻数量 (50%): 相关新闻越多，热度越高")
        lines.append("• 板块权重 (30%): 板块的重要程度")
        lines.append("• 标题质量 (20%): 标题中是否明确包含板块")
        lines.append("")
        lines.append("数据来源：通过搜索市场热点关键词获取")
        lines.append("• 自动提取板块信息")
        lines.append("• 智能过滤和规范化")
        lines.append("• 仅供参考，不构成投资建议")
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
    
    def analyze(self, search_results: List[Dict]) -> List[Dict]:
        """分析搜索结果"""
        logger.info("=" * 60)
        logger.info("开始分析市场热点")
        logger.info("=" * 60)
        logger.info("")
        
        # 步骤 1: 提取板块
        logger.info("[步骤 1/3] 从搜索结果中提取板块...")
        sector_news = self.extract_sectors_from_results(search_results)
        
        extracted_sectors = list(sector_news.keys())
        logger.info(f"  ✓ 提取到 {len(extracted_sectors)} 个板块: {', '.join(extracted_sectors[:10])}")
        
        # 步骤 2: 计算评分
        logger.info("\n[步骤 2/3] 计算热度评分...")
        hotspots = self.calculate_hotspot_scores(sector_news)
        
        logger.info(f"  ✓ 识别出 {len(hotspots)} 个热点板块")
        for idx, hotspot in enumerate(hotspots[:5], 1):
            logger.info(f"    {idx}. {hotspot['sector']} ({hotspot['score']:.1f}分)")
        
        # 步骤 3: 生成报告
        logger.info("\n[步骤 3/3] 生成分析报告...")
        report = self.format_text_report(hotspots)
        
        # 保存结果
        self.save_results(hotspots, report)
        
        return hotspots


def main():
    """主函数"""
    # 示例：使用搜索结果
    # 注意：这些应该是通过搜索 "市场热点"、"热门板块" 等关键词获取的真实数据
    
    sample_search_results = [
        {
            'title': '人工智能板块今日表现强劲，ChatGPT概念全线飘红',
            'content': '受ChatGPT、算力等利好消息影响，人工智能板块今日表现强劲，多只个股涨停。',
            'url': 'https://example.com/news/1'
        },
        {
            'title': '新能源板块大涨，光伏龙头股涨停',
            'content': '国家出台新能源支持政策，光伏、风电等板块应声大涨。光伏龙头股涨停，储能概念股全线飘红。',
            'url': 'https://example.com/news/2'
        },
        {
            'title': '半导体板块活跃，国产替代加速推进',
            'content': '半导体板块今日活跃，国产替代加速推进。芯片、设备等细分领域表现优异。',
            'url': 'https://example.com/news/3'
        },
        {
            'title': '医药板块反弹，创新药表现亮眼',
            'content': '医药板块今日出现反弹，创新药表现亮眼。医疗器械、疫苗等细分领域均有上涨。',
            'url': 'https://example.com/news/4'
        },
        {
            'title': '消费板块回暖，白酒家电领涨',
            'content': '消费板块今日回暖，白酒、家电领涨。免税、零售等细分领域跟随上涨。',
            'url': 'https://example.com/news/5'
        },
        {
            'title': '军工板块活跃，卫星导航概念走强',
            'content': '军工板块今日活跃，卫星导航概念走强。军工龙头股成交量放大。',
            'url': 'https://example.com/news/6'
        },
        {
            'title': '通信板块上涨，5G 概念表现强势',
            'content': '通信板块今日上涨，5G 概念表现强势。通信龙头股资金净流入。',
            'url': 'https://example.com/news/7'
        },
        {
            'title': '汽车板块活跃，新能源车概念走强',
            'content': '汽车板块今日活跃，新能源车、智能驾驶等细分领域走强。',
            'url': 'https://example.com/news/8'
        },
        {
            'title': '金融板块稳定，银行保险小幅上涨',
            'content': '金融板块今日表现稳定，银行、保险小幅上涨。金融板块估值处于历史低位。',
            'url': 'https://example.com/news/9'
        },
        {
            'title': '人工智能板块持续走强，AI 概念股涨停',
            'content': '人工智能板块持续走强，AI、大模型等概念股涨停。算力概念股表现突出。',
            'url': 'https://example.com/news/10'
        },
        {
            'title': '新能源板块政策利好，风电概念大涨',
            'content': '新能源板块继续上涨，风电概念股大涨。政策持续利好新能源。',
            'url': 'https://example.com/news/11'
        },
        {
            'title': '半导体板块国产化加速，芯片概念股走强',
            'content': '半导体板块国产化加速，芯片概念股走强。集成电路板块表现优异。',
            'url': 'https://example.com/news/12'
        },
        {
            'title': '医药板块创新高，创新药龙头涨停',
            'content': '医药板块创新高，创新药龙头涨停。疫苗、医疗器械等细分领域均有表现。',
            'url': 'https://example.com/news/13'
        },
        {
            'title': '消费板块持续回暖，白酒龙头涨停',
            'content': '消费板块持续回暖，白酒龙头涨停。家电、零售、免税等细分领域跟随上涨。',
            'url': 'https://example.com/news/14'
        },
        {
            'title': '通信板块5G 概念持续走强，基站建设加速',
            'content': '通信板块5G 概念持续走强，基站建设加速。光纤、光通信等细分领域表现优异。',
            'url': 'https://example.com/news/15'
        }
    ]
    
    extractor = OptimizedHotspotExtractor()
    hotspots = extractor.analyze(sample_search_results)
    
    print("\n" + extractor.format_text_report(hotspots))


if __name__ == "__main__":
    main()
