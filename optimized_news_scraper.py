"""
真实新闻抓取器 - 优化版

增加更多错误处理和备用方案
"""

import requests
from bs4 import BeautifulSoup
import logging
import time
from datetime import datetime
from typing import Dict, List
from collections import Counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OptimizedNewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # 财经新闻网站列表（增加更多来源）
        self.news_sources = {
            '东方财富': {
                'url': 'https://finance.eastmoney.com/a/cjyw.html',
                'article_selectors': ['.news-item', 'li', '.article'],
                'title_selector': ['a', 'h3', '.title']
            },
            '新浪财经': {
                'url': 'https://finance.sina.com.cn/roll/',
                'article_selectors': ['.list_14 ul li', 'li', '.article'],
                'title_selector': ['a', 'h3', '.title']
            },
            '网易财经': {
                'url': 'https://money.163.com/special/00252MG4/stock.html',
                'article_selectors': ['.news-list li', 'li', '.article'],
                'title_selector': ['a', 'h3', '.title']
            },
            '同花顺': {
                'url': 'https://news.10jqka.com.cn/',
                'article_selectors': ['.news-item', 'li', '.article'],
                'title_selector': ['a', 'h3', '.title']
            },
            '证券之星': {
                'url': 'https://www.stockstar.com/',
                'article_selectors': ['.news-item', 'li', '.article'],
                'title_selector': ['a', 'h3', '.title']
            },
            '和讯网': {
                'url': 'https://www.hexun.com/',
                'article_selectors': ['.news-item', 'li', '.article'],
                'title_selector': ['a', 'h3', '.title']
            }
        }
        
        # 板块关键词
        self.sector_keywords = {
            '人工智能': ['AI', '人工智能', '大模型', 'ChatGPT', '算力', '机器学习', '深度学习', '智能', '自动化'],
            '新能源': ['新能源', '光伏', '风电', '储能', '锂电', '充电桩', '氢能', '电池', '太阳能', '风电叶片'],
            '半导体': ['芯片', '半导体', '集成电路', '存储', '封测', '晶圆', '晶片', '电子'],
            '医药': ['医药', '医疗', '疫苗', '创新药', '医疗器械', '生物制药', '制药', '药业'],
            '消费': ['消费', '白酒', '家电', '食品', '零售', '免税', '乳业', '啤酒', '商业', '零售'],
            '金融': ['银行', '证券', '保险', '金融', '信托', '期货', '券商', '资管', '理财'],
            '地产': ['地产', '房地产', '物业管理', '基建', '建材', '水泥', '钢铁', '建筑'],
            '军工': ['军工', '航天', '卫星', '国防', '导弹', '航空', '航天器', '导弹', '装备'],
            '通信': ['通信', '5G', '6G', '基站', '光通信', '光纤', '通信设备', '电信', '通讯'],
            '汽车': ['汽车', '新能源车', '智能驾驶', '激光雷达', '车联网', '自动驾驶', '整车'],
            '有色': ['有色', '铜', '铝', '黄金', '白银', '贵金属', '稀土', '镍', '锌', '铅'],
        }
        
        # 板块权重
        self.sector_weights = {
            '人工智能': 1.5,
            '新能源': 1.5,
            '半导体': 1.3,
            '医药': 1.2,
            '金融': 1.2,
            '军工': 1.3,
            '通信': 1.1,
            '消费': 1.1,
            '汽车': 1.1,
            '地产': 1.0,
            '有色': 1.0,
        }

    def fetch_news_from_source(self, source_name: str, source_config: Dict, max_articles: int = 50) -> List[Dict]:
        """从指定新闻源抓取新闻"""
        logger.info(f"从 {source_name} 抓取新闻...")
        
        try:
            response = self.session.get(source_config['url'], timeout=20)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                logger.warning(f"  HTTP {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            news_list = []
            
            # 尝试多个选择器
            for article_selector in source_config['article_selectors']:
                articles = soup.select(article_selector)
                
                if not articles:
                    continue
                
                logger.info(f"  使用选择器: {article_selector}, 找到 {len(articles)} 个元素")
                
                for idx, article in enumerate(articles[:max_articles]):
                    try:
                        # 尝试多个标题选择器
                        title = ''
                        url = ''
                        time_str = ''
                        
                        for title_selector in source_config['title_selector']:
                            title_elem = article.select_one(title_selector)
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                                url = title_elem.get('href', '')
                                break
                        
                        # 如果没有找到标题，尝试从整个元素中提取
                        if not title:
                            all_text = article.get_text(strip=True)
                            if len(all_text) > 5 and len(all_text) < 100:
                                title = all_text
                        
                        # 提取链接
                        if not url and title:
                            all_links = article.find_all('a')
                            if all_links:
                                url = all_links[0].get('href', '')
                        
                        # 处理 URL
                        if url and not url.startswith('http'):
                            base_url = source_config['url'].split('/')[0] + '//' + source_config['url'].split('/')[2]
                            if url.startswith('/'):
                                url = base_url + url
                        
                        # 提取时间
                        time_str = datetime.now().strftime('%H:%M')
                        
                        if title:
                            news_list.append({
                                'title': title,
                                'url': url,
                                'source': source_name,
                                'time': time_str,
                                'timestamp': datetime.now().isoformat()
                            })
                    
                    except Exception as e:
                        logger.warning(f"    解析文章 {idx} 失败: {e}")
                        continue
                
                if news_list:
                    break  # 找到新闻就停止尝试其他选择器
            
            logger.info(f"  ✓ 获取到 {len(news_list)} 条新闻")
            time.sleep(0.5)  # 避免请求过快
            
            return news_list
        
        except requests.exceptions.RequestException as e:
            logger.error(f"  ✗ 网络请求失败: {e}")
            return []
        except Exception as e:
            logger.error(f"  ✗ 解析失败: {e}")
            import traceback
            traceback.print_exc()
            return []

    def fetch_all_news(self) -> List[Dict]:
        """从所有新闻源获取新闻"""
        logger.info("=" * 80)
        logger.info("开始获取财经新闻")
        logger.info("=" * 80)
        logger.info("")
        
        all_news = []
        
        for idx, (source_name, source_config) in enumerate(self.news_sources.items(), 1):
            logger.info(f"[{idx}/{len(self.news_sources)}] 抓取 {source_name}...")
            news_list = self.fetch_news_from_source(source_name, source_config)
            
            if news_list:
                logger.info(f"  ✓ {source_name}: {len(news_list)} 条")
                all_news.extend(news_list)
            else:
                logger.warning(f"  ✗ {source_name}: 未获取到新闻")
            
            logger.info("")
        
        # 去重
        seen_titles = set()
        unique_news = []
        
        for news in all_news:
            title = news.get('title', '')
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(news)
        
        logger.info(f"总计获取到 {len(unique_news)} 条新闻（去重后）")
        
        return unique_news

    def extract_sectors_from_news(self, news_list: List[Dict]) -> Dict[str, List]:
        """从新闻中提取板块"""
        logger.info("")
        logger.info("从新闻中提取热点板块...")
        logger.info("")
        
        sector_news = {}
        
        for news in news_list:
            title = news.get('title', '').lower()
            full_text = title
            
            # 检查每个板块
            for sector, keywords in self.sector_keywords.items():
                match_count = sum(1 for keyword in keywords if keyword.lower() in title)
                
                if match_count > 0:
                    if sector not in sector_news:
                        sector_news[sector] = []
                    
                    # 检查是否重复
                    existing_titles = [n.get('title', '') for n in sector_news[sector]]
                    if title not in existing_titles:
                        sector_news[sector].append({
                            'title': news.get('title', ''),
                            'url': news.get('url', ''),
                            'source': news.get('source', ''),
                            'time': news.get('time', '')
                        })
        
        # 统计每个板块的新闻数量
        sector_stats = {}
        for sector, news in sector_news.items():
            sector_stats[sector] = {
                'count': len(news),
                'news': news
            }
        
        logger.info(f"识别出 {len(sector_stats)} 个板块")
        top_sectors = sorted(sector_stats.items(), key=lambda x: x[1]['count'], reverse=True)
        
        for idx, (sector, stat) in enumerate(top_sectors[:8], 1):
            logger.info(f"  {idx}. {sector}: {stat['count']} 条新闻")
        
        return sector_stats

    def calculate_hotspot_scores(self, sector_stats: Dict) -> List[Dict]:
        """计算热点评分"""
        logger.info("")
        logger.info("计算热点评分...")
        logger.info("")
        
        hotspots = []
        
        for sector, stat in sector_stats.items():
            news_count = stat.get('count', 0)
            
            if news_count == 0:
                continue
            
            # 1. 新闻数量分数 (50%)
            news_score = min(100, news_count * 3)
            
            # 2. 板块权重分数 (30%)
            weight = self.sector_weights.get(sector, 1.0)
            weight_score = weight * 30
            
            # 3. 时效性分数 (20%)
            # 检查新闻的新鲜度
            fresh_count = 0
            for news in stat['news']:
                time_str = news.get('time', '')
                try:
                    hour = int(time_str.split(':')[0]) if ':' in time_str else 12
                    if hour >= 9 and hour <= 15:  # 白天新闻
                        fresh_count += 1
                except:
                    pass
            
            fresh_ratio = fresh_count / news_count if news_count > 0 else 0
            freshness_score = 20 * fresh_ratio
            
            # 综合评分
            total_score = news_score * 0.5 + weight_score * 0.3 + freshness_score * 0.2
            
            # 选择代表性新闻
            representative_news = stat['news'][:3]
            
            hotspots.append({
                'sector': sector,
                'score': round(total_score, 1),
                'news_count': news_count,
                'sector_weight': weight,
                'freshness_score': round(freshness_score, 1),
                'related_news': representative_news
            })
        
        # 按评分排序
        hotspots.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"计算完成，识别出 {len(hotspots)} 个热点板块")
        for idx, hotspot in enumerate(hotspots[:5], 1):
            logger.info(f"  {idx}. {hotspot['sector']}: {hotspot['score']:.1f}分")
        
        return hotspots[:10]

    def format_text_report(self, hotspots: List[Dict], news_list: List[Dict]) -> str:
        """生成文本报告"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"                    市场热点分析报告")
        lines.append(f"              {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"数据来源：")
        lines.append(f"  • 新闻总数：{len(news_list)} 条")
        lines.append(f"  • 覆盖网站：{', '.join(list(self.news_sources.keys()))}")
        lines.append("")
        lines.append(f"分析方法：")
        lines.append(f"  1. 从 {len(self.news_sources)} 个财经网站抓取新闻")
        lines.append(f"  2. 从新闻标题中智能提取板块")
        lines.append(f"  3. 按新闻数量、板块权重、时效性综合评分")
        lines.append("")
        
        if hotspots:
            for idx, hotspot in enumerate(hotspots, 1):
                lines.append(f"【{idx}】{hotspot['sector']}")
                lines.append(f"    热度评分: {hotspot['score']:.1f}")
                lines.append(f"    评分明细：")
                lines.append(f"      • 新闻数量: {hotspot['news_count']} 条 (50%权重)")
                lines.append(f"      • 板块权重: {hotspot['sector_weight']} (30%权重)")
                lines.append(f"      • 时效性: {hotspot['freshness_score']:.1f} (20%权重)")
                lines.append(f"    相关新闻 ({min(3, len(hotspot.get('related_news', [])))} 条):")
                
                for news in hotspot.get('related_news', [])[:3]:
                    lines.append(f"      • {news['title'][:70]}")
                    lines.append(f"        来源: {news['source']} | 时间: {news['time']}")
                    lines.append(f"        链接: {news['url']}")
                
                lines.append("")
        
        lines.append("=" * 80)
        lines.append("使用说明：")
        lines.append("• 本报告基于真实财经网站新闻分析")
        lines.append("• 通过智能提取板块和综合评分识别热点")
        lines.append("• 仅供参考，不构成投资建议")
        lines.append("• 投资有风险，入市需谨慎")
        lines.append("=" * 80)
        
        return '\n'.join(lines)

    def save_results(self, hotspots: List[Dict], news_list: List[Dict], report: str):
        """保存结果"""
        import os
        import json
        
        os.makedirs('data', exist_ok=True)
        
        # 保存新闻数据
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        news_file = f"data/news_{timestamp}.json"
        
        with open(news_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'news_count': len(news_list),
                'sources': list(self.news_sources.keys()),
                'news': news_list
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"新闻数据已保存: {news_file}")
        
        # 保存热点数据
        hotspots_file = f"data/hotspots_{timestamp}.json"
        
        with open(hotspots_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'hotspots_count': len(hotspots),
                'hotspots': hotspots
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"热点数据已保存: {hotspots_file}")
        
        # 保存报告
        report_file = f"data/hotspots_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"分析报告已保存: {report_file}")
        
        return {
            'news_file': news_file,
            'hotspots_file': hotspots_file,
            'report_file': report_file
        }

    def run(self):
        """执行完整流程"""
        logger.info("=" * 80)
        logger.info("                    真实新闻抓取与热点分析")
        logger.info(f"              {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        logger.info("=" * 80)
        logger.info("")
        
        # 步骤 1: 抓取新闻
        news_list = self.fetch_all_news()
        
        if not news_list:
            logger.error("未获取到任何新闻，无法分析")
            logger.info("")
            logger.info("建议：")
            logger.info("1. 检查网络连接")
            logger.info("2. 检查网站是否可访问")
            logger.info("3. 尝试使用内置示例数据")
            logger.info("4. 或者手动输入搜索结果")
            return None
        
        # 步骤 2: 提取板块
        sector_stats = self.extract_sectors_from_news(news_list)
        
        # 步骤 3: 计算评分
        hotspots = self.calculate_hotspot_scores(sector_stats)
        
        # 步骤 4: 生成报告
        report = self.format_text_report(hotspots, news_list)
        
        # 步骤 5: 保存结果
        files = self.save_results(hotspots, news_list, report)
        
        # 显示报告
        logger.info("\n" + report)
        
        logger.info("\n" + "=" * 80)
        logger.info("抓取与分析完成！")
        logger.info("=" * 80)
        logger.info("")
        logger.info("生成文件：")
        logger.info(f"  • 新闻数据: {files['news_file']}")
        logger.info(f"  • 热点数据: {files['hotspots_file']}")
        logger.info(f"  • 分析报告: {files['report_file']}")
        logger.info("")
        
        logger.info("下一步：")
        logger.info("1. 查看热点分析报告")
        logger.info("2. 将热点板块用于股票筛选")
        logger.info("3. 在投资报告中展示热点信息")
        
        return hotspots


if __name__ == "__main__":
    scraper = OptimizedNewsScraper()
    scraper.run()
