# 市场热点收集器使用指南

## 功能说明

市场热点收集器通过搜索和分析财经信息，识别当前的市场热点板块。

## 核心组件

### 1. hotspot_analyzer.py（推荐使用）

基于搜索结果进行热点分析。

**特点**：
- ✅ 支持自定义搜索结果
- ✅ 可配合 MCP websearch 使用
- ✅ 智能提取热点板块
- ✅ 生成文本报告和 JSON 数据
- ✅ 无需网络，可离线使用

### 2. hotspot_searcher.py

通过 AKShare 获取实时数据。

**特点**：
- ✅ 实时获取热门板块
- ✅ 实时获取概念板块
- ✅ 统计涨停板股票
- ⚠️ 需要网络连接

### 3. hotspot_collector.py

通过网页抓取获取财经新闻。

**特点**：
- ✅ 多源新闻抓取
- ✅ 关键词提取
- ⚠️ 需要稳定的网络
- ⚠️ 网页结构变化可能导致失效

## 使用方法

### 方法 1：使用 MCP websearch（推荐）

#### 步骤 1：搜索市场热点

使用 MCP websearch 搜索以下关键词：
```
"A股 市场热点 最新"
"股市 题材概念"
"热点板块"
"主线题材"
```

#### 步骤 2：获取搜索结果

将搜索结果整理为以下格式：
```python
search_results = [
    {
        'title': '人工智能板块持续走强，多只个股涨停',
        'content': '受利好消息影响，人工智能板块今日表现强劲...',
        'url': 'https://example.com/news/1'
    },
    {
        'title': '新能源政策利好，光伏板块大涨',
        'content': '国家出台新能源支持政策...',
        'url': 'https://example.com/news/2'
    }
]
```

#### 步骤 3：分析热点

```python
from hotspot_analyzer import HotspotAnalyzer

analyzer = HotspotAnalyzer()

# 分析搜索结果
hotspots = analyzer.analyze_search_results(search_results)

# 生成报告
report = analyzer.format_text_report(hotspots)

# 保存结果
analyzer.save_results(hotspots, report)

# 显示报告
print(report)
```

### 方法 2：使用实时数据（需要网络）

```bash
python hotspot_searcher.py
```

### 方法 3：使用网页抓取（需要网络）

```bash
python hotspot_collector.py
```

## 输出格式

### 1. JSON 数据

保存在 `data/hotspots_YYYYMMDD_HHMMSS.json`：

```json
{
  "timestamp": "2026-01-28T11:31:48.123456",
  "hotspots": [
    {
      "sector": "新能源",
      "score": 50.0,
      "match_count": 5,
      "related_news": [
        {
          "title": "新能源政策利好，光伏板块大涨",
          "url": "https://example.com/news/2",
          "snippet": "国家出台新能源支持政策..."
        }
      ]
    }
  ]
}
```

### 2. 文本报告

保存在 `data/hotspots_report_YYYYMMDD_HHMMSS.txt`：

```
================================================================================
                    市场热点分析报告
              2026年01月28日 11:31
================================================================================

【1】新能源
    热度评分: 50.0
    匹配次数: 5
    相关新闻 (1 条):
      • 新能源政策利好，光伏板块大涨
        https://example.com/news/2

【2】人工智能
    热度评分: 30.0
    匹配次数: 3
    相关新闻 (1 条):
      • 人工智能板块持续走强，多只个股涨停
        https://example.com/news/1
================================================================================
```

## 热点板块定义

系统识别以下板块：

| 板块 | 关键词 |
|------|----------|
| 人工智能 | AI、人工智能、大模型、ChatGPT、算力 |
| 新能源 | 新能源、光伏、风电、储能、锂电、充电桩 |
| 半导体 | 芯片、半导体、集成电路、存储、封测 |
| 医药 | 医药、医疗、疫苗、创新药、医疗器械 |
| 消费 | 消费、白酒、家电、食品、零售、免税 |
| 金融 | 银行、证券、保险、金融、信托、期货 |
| 地产 | 地产、房地产、物业管理、基建、建材 |
| 军工 | 军工、航天、卫星、国防、导弹 |
| 通信 | 通信、5G、6G、基站、光通信 |
| 汽车 | 汽车、新能源车、智能驾驶、激光雷达 |

## 评分规则

热点评分综合考虑：
1. **匹配次数** (50%): 关键词在搜索结果中出现的次数
2. **相关新闻数量** (30%): 相关新闻的条数
3. **新闻时效性** (20%): 新闻的发布时间

评分越高，表示该板块热度越高。

## 集成到主程序

### 1. 获取热点数据

```python
from hotspot_analyzer import HotspotAnalyzer
import json

# 加载搜索结果（可以来自 MCP websearch）
with open('search_results.json', 'r') as f:
    search_results = json.load(f)

# 分析热点
analyzer = HotspotAnalyzer()
hotspots = analyzer.analyze_search_results(search_results)
```

### 2. 结合股票分析

将识别的热点板块用于股票筛选：
```python
# 根据热点板块筛选股票
hotspot_sectors = [h['sector'] for h in hotspots]

# 筛选相关股票
stocks_in_hotspot = []
for stock in all_stocks:
    if stock.get('sector') in hotspot_sectors:
        stocks_in_hotspot.append(stock)
```

### 3. 生成投资建议

针对热点板块内的股票进行分析和推荐。

## 网络问题解决方案

如果遇到网络连接问题：

1. **使用热点分析器** (`hotspot_analyzer.py`)
   - 无需网络
   - 只需要搜索结果
   - 配合 MCP websearch 使用

2. **检查代理设置**
   ```bash
   echo $HTTP_PROXY
   echo $HTTPS_PROXY
   ```

3. **临时禁用代理**
   ```bash
   unset HTTP_PROXY
   unset HTTPS_PROXY
   python hotspot_searcher.py
   ```

## 测试

### 测试热点分析器

```bash
cd auto-investment-advisor
python hotspot_analyzer.py
```

这将运行示例，展示如何使用热点分析器。

### 完整测试

```bash
# 1. 使用 MCP websearch 搜索（手动）
# 搜索："A股 市场热点 最新"

# 2. 保存搜索结果为 JSON
# 保存为：search_results.json

# 3. 运行分析
python hotspot_analyzer.py
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `hotspot_analyzer.py` | 热点分析器（推荐使用）|
| `hotspot_searcher.py` | 实时数据搜索器 |
| `hotspot_collector.py` | 新闻抓取器 |
| `test_hotspot.py` | 测试脚本 |

## 注意事项

1. **MCP websearch**：需要配置 MCP 服务
2. **网络限制**：某些数据源可能需要 VPN
3. **数据时效性**：热点分析基于搜索结果，请确保数据及时
4. **仅供参考**：热点分析仅供参考，不构成投资建议

## 常见问题

### Q: 如何获取搜索结果？

A: 使用 MCP websearch 搜索以下关键词：
- "A股 市场热点 最新"
- "股市 题材概念"
- "热点板块"
- "主线题材"

### Q: 搜索结果格式是什么？

A: 每个结果包含：
- `title`: 新闻标题
- `content`: 新闻内容摘要
- `url`: 新闻链接

### Q: 如何自定义热点板块？

A: 修改 `hotspot_analyzer.py` 中的 `sector_keywords` 字典。

### Q: 热点评分如何计算？

A: 综合考虑匹配次数、相关新闻数量、新闻时效性。
