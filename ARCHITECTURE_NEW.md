# 项目架构说明

## 模块化设计

项目已分为两个独立模块：

### 1. 数据获取模块 (`fetch_data.py`)

**功能**：
- 获取三大市场（A股、港股、美股）的实时数据
- 收集热门股票、板块信息
- 将数据保存为 JSON 文件

**输出**：
- `data/market_data_YYYYMMDD_HHMMSS.json`

**运行方式**：
```bash
python fetch_data.py
# 或
RUN_MODE=fetch python main.py
```

### 2. 股票分析模块 (`analyze_stocks.py`)

**功能**：
- 加载市场数据
- 对每只股票进行基本面和技术面分析
- 生成投资建议
- 生成 HTML 报告
- 发送邮件推送

**输入**：
- `data/market_data_YYYYMMDD_HHMMSS.json`

**输出**：
- `data/recommendations_YYYYMMDD_HHMMSS.json`
- `reports/report_YYYYMMDD_HHMMSS.html`

**运行方式**：
```bash
# 使用最新的数据文件
python analyze_stocks.py

# 或指定数据文件
python analyze_stocks.py data/market_data_20240127_160000.json

# 或通过 main.py
RUN_MODE=analyze python main.py
```

### 3. 完整流程 (`main.py`)

**功能**：
- 依次运行数据获取和股票分析

**运行方式**：
```bash
# 完整流程
python main.py

# 或
RUN_MODE=full python main.py
```

## 数据流

```
fetch_data.py
    ↓
data/market_data_YYYYMMDD_HHMMSS.json
    ↓
analyze_stocks.py
    ├─→ data/recommendations_YYYYMMDD_HHMMSS.json
    └─→ reports/report_YYYYMMDD_HHMMSS.html
         ↓
    邮件推送
```

## GitHub Actions 工作流

### Job 1: fetch-data
- 获取市场数据
- 保存到 artifacts
- 传递给下一个 job

### Job 2: analyze-stocks
- 依赖 fetch-data
- 下载市场数据
- 分析股票并生成报告
- 发送邮件
- 保存报告到 artifacts

## 目录结构

```
auto-investment-advisor/
├── data/                           # 数据存储目录（不提交）
│   ├── market_data_*.json          # 市场数据
│   └── recommendations_*.json       # 推荐数据
├── reports/                        # 报告存储目录（不提交）
│   └── report_*.html              # HTML 报告
├── fetch_data.py                  # 数据获取模块
├── analyze_stocks.py              # 股票分析模块
├── main.py                        # 主程序入口
└── ...
```

## 优势

1. **模块化**：数据获取和股票分析独立，互不影响
2. **灵活性**：可以单独运行任一模块
3. **可测试**：可以使用历史数据进行分析测试
4. **可扩展**：容易添加新的数据源或分析模块
5. **容错性**：数据获取失败不影响已有数据的分析
6. **调试友好**：可以单独调试数据获取或分析逻辑

## 使用场景

### 场景 1：完整流程
```bash
python main.py
```

### 场景 2：只获取数据
```bash
python fetch_data.py
```

### 场景 3：使用历史数据重新分析
```bash
# 1. 获取数据
python fetch_data.py

# 2. 使用特定数据文件分析
python analyze_stocks.py data/market_data_20240127_160000.json
```

### 场景 4：定时任务
GitHub Actions 会自动：
1. 先运行 fetch_data
2. 再运行 analyze_stocks
3. 发送邮件

## 配置说明

### 环境变量 (.env)

新增 `RUN_MODE` 变量：
- `fetch` - 只运行数据获取
- `analyze` - 只运行股票分析
- `full` - 运行完整流程（默认）

## 注意事项

1. **data/ 目录**：在 .gitignore 中，不会被提交到 Git
2. **reports/ 目录**：在 .gitignore 中，不会被提交到 Git
3. **GitHub Artifacts**：数据会在 1 天后自动删除，报告保留 30 天
4. **邮件配置**：只有在 `analyze` 或 `full` 模式下才会发送邮件
