"""
市场热点收集器
通过网络搜索和抓取信息，分析最近的市场热点板块
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import logging
import re
import time
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketHotspotCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # 新闻源配置
        self.news_sources = {
            '东方财富': 'https://finance.eastmoney.com/a/cjyw.html',
            '新浪财经': 'https://finance.sina.com.cn/stock/',
            '网易财经': 'https://money.163.com/special/00252MG4/stock.html',
            '搜狐财经': 'https://business.sohu.com/',
            '同花顺': 'https://news.10jqka.com.cn/',
        }
        
        # 热点关键词
        self.hot_keywords = [
            '热点', '龙头', '暴涨', '涨停', '爆发',
            '概念', '题材', '主线', '风口',
            '政策利好', '消息面', '重大利好'
        ]

    def fetch_news_from_source(self, source_name: str, url: str) -> List[Dict]:
        """从指定新闻源抓取新闻"""
        logger.info(f"从 {source_name} 抓取新闻...")
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news_list = []
            
            # 不同网站的结构不同，需要分别处理
            if 'eastmoney' in url:
                news_list = self._parse_eastmoney(soup)
            elif 'sina' in url:
                news_list = self._parse_sina(soup)
            elif '163' in url:
                news_list = self._parse_163(soup)
            elif 'sohu' in url:
                news_list = self._parse_sohu(soup)
            elif '10jqka' in url:
                news_list = self._parse_10jqka(soup)
            
            logger.info(f"  ✓ 获取到 {len(news_list)} 条新闻")
            time.sleep(1)  # 避免请求过快
            
            return news_list
        except Exception as e:
            logger.error(f"  ✗ 从 {source_name} 获取新闻失败: {e}")
            return []

    def _parse_eastmoney(self, soup: BeautifulSoup) -> List[Dict]:
        """解析东方财富新闻"""
        news_list = []
        items = soup.find_all('li', class_='news-item')
        
        for item in items:
            try:
                title_elem = item.find('a')
                if title_elem:
                    news_list.append({
                        'title': title_elem.get_text(strip=True),
                        'url': title_elem.get('href', ''),
                        'source': '东方财富',
                        'time': self._extract_time(item.get_text())
                    })
            except:
                continue
        
        return news_list

    def _parse_sina(self, soup: BeautifulSoup) -> List[Dict]:
        """解析新浪财经新闻"""
        news_list = []
        items = soup.find_all('li', class_='news-item')
        
        for item in items:
            try:
                title_elem = item.find('a')
                if title_elem:
                    news_list.append({
                        'title': title_elem.get_text(strip=True),
                        'url': title_elem.get('href', ''),
                        'source': '新浪财经',
                        'time': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })
            except:
                continue
        
        return news_list

    def _parse_163(self, soup: BeautifulSoup) -> List[Dict]:
        """解析网易财经新闻"""
        news_list = []
        items = soup.select('.news-item')
        
        for item in items:
            try:
                title_elem = item.find('a')
                if title_elem:
                    news_list.append({
                        'title': title_elem.get_text(strip=True),
                        'url': title_elem.get('href', ''),
                        'source': '网易财经',
                        'time': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })
            except:
                continue
        
        return news_list

    def _parse_sohu(self, soup: BeautifulSoup) -> List[Dict]:
        """解析搜狐财经新闻"""
        news_list = []
        items = soup.select('.news-list li')
        
        for item in items:
            try:
                title_elem = item.find('a')
                if title_elem:
                    news_list.append({
                        'title': title_elem.get_text(strip=True),
                        'url': title_elem.get('href', ''),
                        'source': '搜狐财经',
                        'time': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })
            except:
                continue
        
        return news_list

    def _parse_10jqka(self, soup: BeautifulSoup) -> List[Dict]:
        """解析同花顺新闻"""
        news_list = []
        items = soup.select('.news-item')
        
        for item in items:
            try:
                title_elem = item.find('a')
                if title_elem:
                    news_list.append({
                        'title': title_elem.get_text(strip=True),
                        'url': title_elem.get('href', ''),
                        'source': '同花顺',
                        'time': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })
            except:
                continue
        
        return news_list

    def _extract_time(self, text: str) -> str:
        """从文本中提取时间"""
        # 常见时间格式
        time_patterns = [
            r'\d{2}:\d{2}',  # 10:30
            r'\d{4}-\d{2}-\d{2}',  # 2024-01-28
            r'\d{2}月\d{2}日',  # 01月28日
            r'刚刚',
            r'\d+分钟前',
            r'\d+小时前'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group()
        
        return datetime.now().strftime('%Y-%m-%d %H:%M')

    def fetch_all_news(self) -> List[Dict]:
        """从所有新闻源获取新闻"""
        logger.info("=" * 60)
        logger.info("开始收集财经新闻")
        logger.info("=" * 60)
        
        all_news = []
        
        for source_name, url in self.news_sources.items():
            news_list = self.fetch_news_from_source(source_name, url)
            all_news.extend(news_list)
        
        logger.info(f"\n总计获取到 {len(all_news)} 条新闻")
        return all_news

    def analyze_hotspots(self, news_list: List[Dict]) -> Dict:
        """分析市场热点"""
        logger.info("\n开始分析市场热点...")
        
        # 1. 提取关键词和板块
        sector_keywords = self._extract_sector_keywords(news_list)
        
        # 2. 统计出现频率
        hotspot_stats = self._calculate_hotspot_frequency(sector_keywords)
        
        # 3. 提取相关新闻
        hotspot_news = self._extract_hotspot_news(news_list, hotspot_stats)
        
        # 4. 综合评分
        hotspot_rankings = self._calculate_hotspot_ranking(hotspot_stats, hotspot_news)
        
        logger.info(f"  识别出 {len(hotspot_rankings)} 个热点板块\n")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'hotspots': hotspot_rankings[:10],
            'all_news_count': len(news_list),
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def _extract_sector_keywords(self, news_list: List[Dict]) -> Dict[str, List[str]]:
        """从新闻中提取板块关键词"""
        sector_map = {
            '科技': ['科技', '人工智能', 'AI', '芯片', '半导体', '5G', '物联网', '云计算', '大数据'],
            '新能源': ['新能源', '光伏', '风电', '储能', '锂电池', '电动汽车', '充电桩'],
            '医药': ['医药', '医疗', '生物制药', '疫苗', '创新药', '医疗器械'],
            '消费': ['消费', '白酒', '家电', '食品饮料', '免税', '零售'],
            '金融': ['银行', '证券', '保险', '金融', '信托', '期货'],
            '地产': ['地产', '房地产', '物业管理', '基建', '建材'],
            '军工': ['军工', '航天', '国防', '军工', '卫星'],
            '有色': ['有色', '钢铁', '煤炭', '石油', '天然气'],
            '农业': ['农业', '种业', '养殖', '农机', '农产品'],
            '交通': ['交通', '铁路', '公路', '港口', '航运', '航空'],
        }
        
        sector_keywords = {sector: [] for sector in sector_map.keys()}
        
        for news in news_list:
            title = news.get('title', '')
            
            for sector, keywords in sector_map.items():
                for keyword in keywords:
                    if keyword in title:
                        if keyword not in sector_keywords[sector]:
                            sector_keywords[sector].append({
                                'keyword': keyword,
                                'news_title': title,
                                'news_url': news.get('url', ''),
                                'news_source': news.get('source', '')
                            })
        
        return sector_keywords

    def _calculate_hotspot_frequency(self, sector_keywords: Dict[str, List]) -> List[Dict]:
        """计算热点出现频率"""
        hotspot_stats = []
        
        for sector, items in sector_keywords.items():
            if items:
                hotspot_stats.append({
                    'sector': sector,
                    'keyword_count': len(items),
                    'news_count': len(set(item['news_title'] for item in items)),
                    'keywords': list(set(item['keyword'] for item in items))
                })
        
        # 按频率排序
        hotspot_stats.sort(key=lambda x: x['keyword_count'], reverse=True)
        
        return hotspot_stats

    def _extract_hotspot_news(self, news_list: List[Dict], hotspot_stats: List[Dict]) -> Dict[str, List]:
        """提取热点相关新闻"""
        hotspot_news = {}
        
        top_hotspots = [h['sector'] for h in hotspot_stats[:5]]
        
        for sector in top_hotspots:
            sector_news = []
            
            for news in news_list:
                title = news.get('title', '')
                # 简单匹配
                for keyword in self.hot_keywords:
                    if keyword in title:
                        sector_news.append(news)
                        break
            
            hotspot_news[sector] = sector_news[:5]  # 每个板块最多 5 条
        
        return hotspot_news

    def _calculate_hotspot_ranking(self, hotspot_stats: List[Dict], 
                                    hotspot_news: Dict[str, List]) -> List[Dict]:
        """计算热点排名"""
        rankings = []
        
        for stat in hotspot_stats:
            sector = stat['sector']
            
            # 评分计算
            # 1. 关键词频率 (40%)
            freq_score = min(100, stat['keyword_count'] * 10)
            
            # 2. 新闻数量 (30%)
            news_score = min(100, stat['news_count'] * 5)
            
            # 3. 相关新闻质量 (30%)
            quality_score = 50
            if sector in hotspot_news:
                recent_count = sum(1 for news in hotspot_news[sector] 
                                 if '刚刚' in news.get('time', '') 
                                 or '分钟前' in news.get('time', ''))
                quality_score += recent_count * 10
            
            total_score = freq_score * 0.4 + news_score * 0.3 + quality_score * 0.3
            
            rankings.append({
                'sector': sector,
                'score': round(total_score, 2),
                'keyword_count': stat['keyword_count'],
                'news_count': stat['news_count'],
                'keywords': stat['keywords'],
                'news_sample': hotspot_news.get(sector, [])[:3]
            })
        
        # 按评分排序
        rankings.sort(key=lambda x: x['score'], reverse=True)
        
        return rankings

    def format_hotspots_report(self, analysis_result: Dict) -> str:
        """格式化热点报告"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"                    市场热点分析报告")
        lines.append(f"              {analysis_result.get('analysis_time', '')}")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"新闻来源分析：{analysis_result.get('all_news_count', 0)} 条")
        lines.append(f"识别热点板块：{len(analysis_result.get('hotspots', []))} 个")
        lines.append("")
        
        hotspots = analysis_result.get('hotspots', [])
        
        for idx, hotspot in enumerate(hotspots, 1):
            lines.append(f"【{idx}】{hotspot['sector']}")
            lines.append(f"    热度评分: {hotspot['score']:.1f}")
            lines.append(f"    关键词数: {hotspot['keyword_count']}")
            lines.append(f"    新闻数量: {hotspot['news_count']}")
            lines.append(f"    相关关键词: {', '.join(hotspot['keywords'])}")
            
            if hotspot.get('news_sample'):
                lines.append(f"    相关新闻:")
                for news in hotspot['news_sample']:
                    lines.append(f"      - {news.get('title', '')}")
                    lines.append(f"        {news.get('source', '')} | {news.get('time', '')}")
            
            lines.append("")
        
        lines.append("=" * 80)
        lines.append("分析说明：")
        lines.append("• 基于主流财经媒体的新闻报道分析")
        lines.append("• 通过关键词提取和频率统计识别热点")
        lines.append("• 综合评分考虑热度、时效性和新闻质量")
        lines.append("• 仅供参考，不构成投资建议")
        lines.append("=" * 80)
        
        return '\n'.join(lines)

    def run(self) -> Dict:
        """执行热点收集和分析"""
        # 1. 收集新闻
        news_list = self.fetch_all_news()
        
        if not news_list:
            logger.warning("未获取到新闻，无法分析热点")
            return {}
        
        # 2. 分析热点
        analysis_result = self.analyze_hotspots(news_list)
        
        # 3. 生成报告
        report = self.format_hotspots_report(analysis_result)
        
        logger.info("\n" + report)
        
        # 4. 保存结果
        self.save_results(analysis_result, report)
        
        return analysis_result

    def save_results(self, analysis_result: Dict, report: str):
        """保存分析结果"""
        import os
        import json
        
        os.makedirs('data', exist_ok=True)
        
        # 保存 JSON
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = f"data/hotspots_{timestamp}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"分析结果已保存: {json_file}")
        
        # 保存文本报告
        txt_file = f"data/hotspots_report_{timestamp}.txt"
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"分析报告已保存: {txt_file}")


if __name__ == "__main__":
    collector = MarketHotspotCollector()
    collector.run()
