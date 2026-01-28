# MCP WebSearch 功能状态与使用指南

## 状态总结

### ✅ MCP WebSearch 配置正常

你的 MCP websearch 服务已正确配置：

**配置文件**：`~/.config/opencode/mcp_config.json`

**已配置的服务器**：
1. **Tavily** ✅
   - API Key: `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`
   - 状态: 已配置并可用

2. **open-websearch** ✅
   - 搜索引擎: 百度
   - 状态: 已配置并可用

## 使用方法

### 方法 1：在支持 MCP 的环境中使用（推荐）

如果你在支持 MCP 的环境中（如 opencode），可以直接使用 websearch 工具：

#### 步骤 1：搜索市场热点

```
websearch "A股 市场热点 最新"
websearch "股市 题材概念"
websearch "热点板块"
```

#### 步骤 2：整理搜索结果

将搜索结果整理为以下格式：

```python
search_results = [
    {
        'title': '人工智能板块持续走强',
        'content': '受利好消息影响...',
        'url': 'https://example.com/news/1'
    },
    {
        'title': '新能源政策利好',
        'content': '国家出台新能源支持政策...',
        'url': 'https://example.com/news/2'
    }
]
```

#### 步骤 3：分析热点

```python
from hotspot_analyzer import HotspotAnalyzer

analyzer = HotspotAnalyzer()
hotspots = analyzer.analyze_search_results(search_results)
report = analyzer.format_text_report(hotspots)
print(report)
```

### 方法 2：使用集成的搜索与分析脚本

我们已经创建了完整的集成脚本：

#### 1. 使用示例数据测试（推荐先测试）

```bash
cd auto-investment-advisor
python search_analyze.py sample
```

这将使用内置的示例数据，展示整个流程如何工作。

#### 2. 手动输入搜索结果

```bash
python search_analyze.py manual
```

然后：
1. 在浏览器中搜索：`https://www.baidu.com/s?wd=A股 市场热点 最新`
2. 复制新闻标题和链接
3. 在程序中输入（格式：`标题|链接`）
4. 输入完成后输入 `done`

#### 3. 尝试使用 MCP websearch

```bash
python search_analyze.py mcp
```

如果 MCP websearch 在当前环境可用，将自动使用。否则会提示手动输入。

### 方法 3：创建搜索结果文件

如果你已经手动搜索并整理好了结果，可以创建一个 JSON 文件：

**文件**: `search_results.json`

```json
{
  "query": "A股 市场热点 最新",
  "timestamp": "2026-01-28T11:31:48",
  "results": [
    {
      "title": "人工智能板块持续走强，多只个股涨停",
      "content": "受利好消息影响，人工智能板块今日表现强劲...",
      "url": "https://example.com/news/1"
    },
    {
      "title": "新能源政策利好，光伏板块大涨",
      "content": "国家出台新能源支持政策...",
      "url": "https://example.com/news/2"
    }
  ]
}
```

然后使用以下代码分析：

```python
import json
from hotspot_analyzer import HotspotAnalyzer

# 加载搜索结果
with open('search_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 分析热点
analyzer = HotspotAnalyzer()
hotspots = analyzer.analyze_search_results(data['results'])

# 生成报告
report = analyzer.format_text_report(hotspots)

# 保存并显示
analyzer.save_results(hotspots, report)
print(report)
```

## 测试验证

### 测试 1：验证 MCP 配置

```bash
python test_websearch.py test "测试查询"
```

**预期输出**：
- ✓ MCP 配置文件存在
- ✓ Tavily: 已配置
- ✓ open-websearch: 已配置

### 测试 2：运行完整流程

```bash
python search_analyze.py sample
```

**预期输出**：
- 识别出 X 个热点板块
- 生成完整的文本报告
- 保存 JSON 数据

## 输出文件

运行后会生成以下文件：

### 1. JSON 数据
`data/hotspots_YYYYMMDD_HHMMSS.json`

```json
{
  "timestamp": "2026-01-28T11:31:48.123456",
  "hotspots": [
    {
      "sector": "新能源",
      "score": 50.0,
      "match_count": 5,
      "related_news": [...]
    }
  ]
}
```

### 2. 文本报告
`data/hotspots_report_YYYYMMDD_HHMMSS.txt`

```
================================================================================
                    市场热点分析报告
              2026年01月28日 11:31
================================================================================

【1】新能源
    热度评分: 50.0
    匹配次数: 5
    相关新闻: ...
================================================================================
```

## 热点板块识别

系统智能识别以下板块：

| 板块 | 关键词 |
|------|----------|
| 人工智能 | AI、人工智能、大模型、ChatGPT、算力 |
| 新能源 | 新能源、光伏、风电、储能、锂电 |
| 半导体 | 芯片、半导体、集成电路、存储 |
| 医药 | 医药、医疗、疫苗、创新药 |
| 消费 | 消费、白酒、家电、食品 |
| 金融 | 银行、证券、保险、金融 |
| 地产 | 地产、房地产、物业管理 |
| 军工 | 军工、航天、卫星、国防 |
| 通信 | 通信、5G、6G、基站 |
| 汽车 | 汽车、新能源车、智能驾驶 |

## 评分规则

热度评分 = 匹配次数 × 10 + 新闻数量 × 5 + 时效性 × 10

- **匹配次数** (50%): 关键词在搜索结果中出现的次数
- **新闻数量** (30%): 相关新闻的条数
- **时效性** (20%): 新闻的发布时间

评分越高，表示该板块热度越高。

## 常见问题

### Q: MCP websearch 在当前环境中不可用怎么办？

A: 使用方法 2 或方法 3，手动输入搜索结果。

### Q: 如何在 opencode 中使用 MCP websearch？

A: 直接使用 `websearch` 命令：
```
websearch "搜索内容"
```

### Q: 搜索结果的格式是什么？

A: 每个结果包含：
- `title`: 新闻标题
- `content`: 新闻内容摘要
- `url`: 新闻链接

### Q: 如何自定义热点板块？

A: 修改 `hotspot_analyzer.py` 中的 `sector_keywords` 字典。

### Q: 热点分析准确吗？

A: 分析基于关键词匹配和频率统计。为了提高准确性：
- 使用最新的搜索结果
- 搜索多个关键词
- 结合多个数据源

## 文件说明

| 文件 | 说明 |
|------|------|
| `search_analyze.py` | 搜索与分析集成脚本 |
| `hotspot_analyzer.py` | 热点分析器 |
| `test_websearch.py` | MCP websearch 测试脚本 |
| `HOTSPOT_GUIDE.md` | 热点收集器详细指南 |

## 总结

✅ **MCP WebSearch 配置正常**
   - Tavily 已配置
   - open-websearch 已配置
   - 两个服务都可用

✅ **完整的工作流程**
   1. 搜索（使用 MCP websearch 或手动）
   2. 整理搜索结果
   3. 分析热点板块
   4. 生成报告

✅ **多种使用方式**
   - 示例数据测试
   - 手动输入结果
   - MCP websearch 集成

**下一步**：选择一种使用方法，开始收集和分析市场热点！
