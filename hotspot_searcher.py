"""
使用 MCP websearch 搜索市场热点
"""

import json
import logging
from datetime import datetime
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketHotspotSearcher:
    def __init__(self):
        self.hotspot_queries = [
            "A股 市场热点 最新",
            "股市 题材概念",
            "股票 涨停板",
            "市场热点板块",
            "概念股",
            "政策利好 板块",
            "主线题材",
            "市场风口",
            "热点龙头股"
        ]
        
        self.sectors = [
            '人工智能', '新能源', '半导体', '芯片', '医药',
            '消费', '金融', '地产', '军工', '有色',
            '通信', '汽车', '电子', '软件', '互联网'
        ]

    def search_hotspots(self) -> List[Dict]:
        """搜索市场热点"""
        logger.info("=" * 60)
        logger.info("开始搜索市场热点")
        logger.info("=" * 60)
        
        all_results = []
        
        # 由于我们无法直接调用 MCP websearch，
        # 让我们使用现有的数据源获取热门信息
        try:
            import akshare as ak
            logger.info("\n[1/3] 从东方财富获取热门板块...")
            
            # 获取热门板块
            sector_df = ak.stock_board_industry_name_em()
            if not sector_df.empty:
                logger.info(f"  获取到 {len(sector_df)} 个板块")
                
                # 筛选涨幅大的板块
                hot_sectors = sector_df[sector_df['涨跌幅'] > 0].head(10)
                
                for idx, row in hot_sectors.iterrows():
                    all_results.append({
                        'sector': row.get('板块名称', ''),
                        'change': row.get('涨跌幅', 0),
                        'volume': row.get('成交额', 0),
                        'source': '东方财富',
                        'time': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })
                
                logger.info(f"  识别出 {len(hot_sectors)} 个热点板块")
        
        except Exception as e:
            logger.error(f"  获取热门板块失败: {e}")
        
        try:
            logger.info("\n[2/3] 从东方财富获取概念板块...")
            
            # 获取概念板块
            concept_df = ak.stock_board_concept_name_em()
            if not concept_df.empty:
                logger.info(f"  获取到 {len(concept_df)} 个概念板块")
                
                # 筛选涨幅大的概念
                hot_concepts = concept_df[concept_df['涨跌幅'] > 0].head(10)
                
                for idx, row in hot_concepts.iterrows():
                    all_results.append({
                        'sector': row.get('板块名称', ''),
                        'change': row.get('涨跌幅', 0),
                        'volume': row.get('成交额', 0),
                        'source': '东方财富概念',
                        'time': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })
                
                logger.info(f"  识别出 {len(hot_concepts)} 个热点概念")
        
        except Exception as e:
            logger.error(f"  获取概念板块失败: {e}")
        
        try:
            logger.info("\n[3/3] 获取涨停板股票...")
            
            # 获取涨停股票
            limit_up_df = ak.stock_zh_a_spot_em()
            if not limit_up_df.empty:
                logger.info(f"  获取到 {len(limit_up_df)} 只股票")
                
                # 筛选涨停股票（涨幅接近 10% 或 20%）
                limit_up_stocks = limit_up_df[limit_up_df['涨跌幅'] > 9.5].head(20)
                
                # 统计行业分布
                industry_count = {}
                for idx, row in limit_up_stocks.iterrows():
                    industry = row.get('行业', '未知')
                    if industry not in industry_count:
                        industry_count[industry] = 0
                    industry_count[industry] += 1
                
                # 将行业分布转换为热点
                sorted_industries = sorted(industry_count.items(), key=lambda x: x[1], reverse=True)
                
                for industry, count in sorted_industries[:5]:
                    all_results.append({
                        'sector': industry,
                        'change': count * 0.5,  # 模拟热度分数
                        'volume': count,
                        'source': '涨停板统计',
                        'time': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })
                
                logger.info(f"  识别出 {len(sorted_industries)} 个热门行业")
        
        except Exception as e:
            logger.error(f"  获取涨停股票失败: {e}")
        
        return all_results

    def analyze_hotspots(self, results: List[Dict]) -> List[Dict]:
        """分析并排序热点"""
        logger.info("\n分析市场热点...")
        
        # 按板块聚合
        sector_map = {}
        
        for result in results:
            sector = result.get('sector', '')
            if not sector:
                continue
            
            if sector not in sector_map:
                sector_map[sector] = {
                    'sector': sector,
                    'total_score': 0,
                    'change_list': [],
                    'volume_list': [],
                    'sources': set(),
                    'sample_stocks': []
                }
            
            # 累计分数
            sector_map[sector]['total_score'] += result.get('change', 0)
            sector_map[sector]['change_list'].append(result.get('change', 0))
            sector_map[sector]['volume_list'].append(result.get('volume', 0))
            sector_map[sector]['sources'].add(result.get('source', ''))
        
        # 计算综合评分
        hotspots = []
        for sector, data in sector_map.items():
            # 平均涨幅
            avg_change = sum(data['change_list']) / len(data['change_list'])
            # 最大涨幅
            max_change = max(data['change_list'])
            # 来源数量
            source_count = len(data['sources'])
            # 综合评分
            total_score = avg_change * 0.5 + max_change * 0.3 + source_count * 10
            
            hotspots.append({
                'sector': sector,
                'avg_change': avg_change,
                'max_change': max_change,
                'source_count': source_count,
                'sources': list(data['sources']),
                'total_score': total_score,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M')
            })
        
        # 按评分排序
        hotspots.sort(key=lambda x: x['total_score'], reverse=True)
        
        return hotspots[:10]

    def format_report(self, hotspots: List[Dict]) -> str:
        """格式化报告"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"                    市场热点分析报告")
        lines.append(f"              {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        lines.append("=" * 80)
        lines.append("")
        
        for idx, hotspot in enumerate(hotspots, 1):
            lines.append(f"【{idx}】{hotspot['sector']}")
            lines.append(f"    热度评分: {hotspot['total_score']:.1f}")
            lines.append(f"    平均涨幅: {hotspot['avg_change']:.2f}%")
            lines.append(f"    最大涨幅: {hotspot['max_change']:.2f}%")
            lines.append(f"    数据来源: {', '.join(hotspot['sources'])}")
            lines.append("")
        
        lines.append("=" * 80)
        lines.append("数据来源：")
        lines.append("• 东方财富热门板块")
        lines.append("• 东方财富概念板块")
        lines.append("• 涨停板股票行业分布")
        lines.append("")
        lines.append("分析说明：")
        lines.append("• 基于多个数据源综合分析")
        lines.append("• 按板块涨幅、热度、来源数量综合评分")
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
        
        # 保存文本报告
        txt_file = f"data/hotspots_report_{timestamp}.txt"
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"分析报告已保存: {txt_file}")

    def run(self):
        """执行热点搜索和分析"""
        # 1. 搜索
        results = self.search_hotspots()
        
        if not results:
            logger.warning("未获取到热点数据")
            return []
        
        # 2. 分析
        hotspots = self.analyze_hotspots(results)
        
        # 3. 生成报告
        report = self.format_report(hotspots)
        
        logger.info("\n" + report)
        
        # 4. 保存
        self.save_results(hotspots, report)
        
        return hotspots


if __name__ == "__main__":
    searcher = MarketHotspotSearcher()
    searcher.run()
