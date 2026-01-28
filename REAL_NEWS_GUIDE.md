# 市场热点收集器 - 真实新闻抓取版本

## 功能说明

这个版本使用真实的财经新闻网站，抓取最新的财经新闻，然后智能提取市场热点板块。

## 核心特点

### ✅ 真实数据源

**支持的财经网站**：
1. 新浪财经 - 50条新闻 ✅
2. 同花顺 - 50条新闻 ✅
3. 证券之星 - 41条新闻 ✅
4. 和讯网 - 46条新闻 ✅

**总计**：**156 条实时财经新闻**

### ✅ 智能板块提取

**预定义的板块关键词**：
- 人工智能: AI、大模型、ChatGPT、算力、机器学习
- 新能源: 光伏、风电、储能、锂电、充电桩、氢能
- 半导体: 芯片、半导体、集成电路、存储、封测
- 医药: 医药、医疗、疫苗、创新药、医疗器械
- 消费: 白酒、家电、食品、零售、免税
- 金融: 银行、证券、保险、信托、期货、券商
- 地产: 房地产、物业管理、基建、建材
- 军工: 军工、航天、卫星、国防、导弹
- 通信: 5G、6G、基站、光通信、光纤
- 汽车: 新能源车、智能驾驶、激光雷达
- 有色: 铜、铝、黄金、白银、贵金属

### ✅ 综合评分系统

**评分公式**：
```
热度评分 = 新闻数量分数 × 50% + 板块权重分数 × 30% + 时效性分数 × 20%
```

**各维度**：
1. **新闻数量分数** (50%)
   - 越多新闻，热度越高
   - 最多 100 分（约 33 条新闻）

2. **板块权重分数** (30%)
   - 人工智能: 1.5（权重最高）
   - 新能源: 1.5（权重最高）
   - 半导体: 1.3
   - 医药: 1.2
   - 金融: 1.2
   - 军工: 1.3
   - 其他板块: 1.0-1.1

3. **时效性分数** (20%)
   - 白天新闻（9:00-15:00）权重更高
   - 越新鲜的新闻权重越高

## 测试结果

### 成功识别的热点板块

| 排名 | 板块 | 热度评分 | 相关新闻数 |
|------|------|-----------|-----------|
| 1 | 有色 | 29.5 | 11 |
| 2 | 人工智能 | 26.5 | 6 |
| 3 | 金融 | 22.3 | 5 |
| 4 | 医药 | 17.8 | 2 |
| 5 | 半导体 | 17.2 | 1 |
| 6 | 消费 | 16.9 | 2 |
| 7 | 通信 | 15.4 | 1 |

### 热点板块新闻示例

**人工智能（26.5分）**：
- 千问旗舰推理模型亮相！机构看好AI驱动与国产扩张

**金融（22.3分）**：
- 南山铝业国际午前涨超5%
- 万国黄金集团午前涨超7%

**有色（29.5分）**：
- 南山铝业拟在印尼建设年产25万吨电解铝项目
- 伦敦期铝升至近四年最高水平

## 使用方法

### 运行新闻抓取器

```bash
cd auto-investment-advisor
python optimized_news_scraper.py
```

### 输出文件

运行后会生成以下文件：

1. **新闻数据** - `data/news_YYYYMMDD_HHMMSS.json`
   ```json
   {
     "timestamp": "2026-01-28T12:07:39",
     "news_count": 156,
     "sources": ["新浪财经", "同花顺", "证券之星", "和讯网"],
     "news": [...156条新闻]
   }
   ```

2. **热点数据** - `data/hotspots_YYYYMMDD_HHMMSS.json`
   ```json
   {
     "timestamp": "2026-01-28T12:07:39",
     "hotspots_count": 7,
     "hotspots": [
       {
         "sector": "有色",
         "score": 29.5,
         "news_count": 11,
         "sector_weight": 1.0,
         "freshness_score": 20.0,
         "related_news": [...]
       }
     ]
   }
   ```

3. **分析报告** - `data/hotspots_report_YYYYMMDD_HHMMSS.txt`
   - 完整的文本报告
   - 包含热点排行和新闻详情

## 热点板块说明

### 当前热点分析

**🥇 第一梯队：有色**
- 热度评分: 29.5
- 相关新闻: 11 条
- 主要驱动：铝价、贵金属价格反弹

**🤖 第二梯队：人工智能**
- 热度评分: 26.5
- 相关新闻: 6 条
- 主要驱动：大模型、国产替代

**📊 第三梯队：金融、医药**
- 金融: 22.3 分（5 条新闻）
- 医药: 17.8 分（2 条新闻）
- 主要驱动：政策利好、业绩预增

**📉 关注梯队：半导体、消费、通信**
- 半导体: 17.2 分（1 条新闻）
- 消费: 16.9 分（2 条新闻）
- 通信: 15.4 分（1 条新闻）

## 集成到主程序

### 步骤 1：加载热点数据

```python
import json

# 加载最新热点数据
with open('data/hotspots_*.json', 'r') as f:
    data = json.load(f)
    hotspots = data['hotspots']

# 提取热点板块名称
hotspot_sectors = [h['sector'] for h in hotspots]
```

### 步骤 2：根据热点筛选股票

```python
def filter_stocks_by_hotspots(all_stocks, hotspot_sectors):
    """根据热点板块筛选股票"""
    filtered = []
    
    for stock in all_stocks:
        sector = stock.get('sector', '')
        if sector in hotspot_sectors:
            # 标记该股票所属热点
            hotpot_rank = hotspot_sectors.index(sector) + 1
            stock['hotpot_rank'] = hotpot_rank
            stock['is_hotspot'] = True
            filtered.append(stock)
    
    return filtered
```

### 步骤 3：在投资报告中展示热点

```python
def generate_report_with_hotspots(market_data, hotspots):
    """生成包含热点信息的投资报告"""
    
    report_parts = []
    
    # 添加热点板块部分
    if hotspots:
        lines.append("┌" + "─" * 60 + "┐")
        lines.append("│" + " " * 18 + "🔥 市场热点" + " " * 35 + "│")
        lines.append("└" + "─" * 60 + "┘")
        lines.append("")
        
        for idx, hotspot in enumerate(hotspots[:5], 1):
            lines.append(f"【{idx}】{hotspot['sector']}")
            lines.append(f"    热度评分: {hotspot['score']:.1f}")
            lines.append(f"    相关新闻: {hotspot['news_count']} 条")
            
            if hotspot.get('related_news'):
                lines.append(f"    代表新闻:")
                for news in hotspot['related_news'][:2]:
                    lines.append(f"      • {news['title'][:60]}")
            
            lines.append("")
    
    report_parts.append('\n'.join(lines))
    
    return '\n\n'.join(report_parts)
```

## 优势总结

### ✅ 真实数据
- 从真实财经网站抓取
- 156 条实时新闻
- 4 个权威财经数据源

### ✅ 智能提取
- 自动识别热点板块
- 智能关键词匹配
- 自动去重和过滤

### ✅ 科学评分
- 多维度综合评分
- 新闻数量、板块权重、时效性
- 权重可配置调整

### ✅ 易于使用
- 一键运行
- 自动生成报告
- JSON 格式方便集成

### ✅ 实时更新
- 可定时运行
- 获取最新热点
- 数据可追溯

## 下一步

### 1. 查看热点分析报告

```bash
cat data/hotspots_report_*.txt
```

### 2. 使用热点筛选股票

将提取的热点板块用于：
- 筛选相关股票
- 优先推荐热点板块内的优质股票
- 在投资报告中突出显示

### 3. 集成到主程序

将热点信息添加到：
- 每日报告中的热点部分
- 股票筛选逻辑
- 投资建议生成

## 文件说明

| 文件 | 说明 |
|------|------|
| `optimized_news_scraper.py` | 真实新闻抓取器（推荐使用） |
| `real_news_scraper.py` | 早期版本（已废弃） |
| `hotspot_extractor_v2.py` | 基于搜索的提取器 |
| `HOTSPOT_SUMMARY.md` | 热点收集器总结 |

## 技术细节

### 新闻抓取

**使用的库**：
- `requests` - HTTP 请求
- `BeautifulSoup` - HTML 解析

**抓取策略**：
- 尝试多个 CSS 选择器
- 自动提取标题和链接
- 自动去重
- 延时避免封禁

### 板块提取

**关键词匹配**：
- 精确匹配关键词
- 多种同义词支持
- 自动规范化板块名称

### 评分算法

```python
total_score = news_score * 0.5 + weight_score * 0.3 + freshness_score * 0.2

其中:
- news_score = min(100, news_count * 3)     # 新闻数量
- weight_score = sector_weight * 30            # 板块权重
- freshness_score = 20 * fresh_ratio           # 时效性
```

## 已推送到 GitHub

所有代码已推送到：
https://github.com/kindlove3218/auto-investment-advisor

**包含的提交**：
- ✅ 优化后的新闻抓取器
- ✅ 真实财经网站新闻抓取
- ✅ 智能热点板块提取
- ✅ 综合评分系统
- ✅ 156 条实时财经新闻
- ✅ 7 个热点板块识别
- ✅ 完整的使用文档

**需要我帮你集成到主程序吗？**
