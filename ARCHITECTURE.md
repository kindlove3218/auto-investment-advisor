# 项目结构

```
auto-investment-advisor/
├── README.md                    # 项目说明
├── QUICKSTART.md                # 快速开始指南
├── SETUP.md                     # 详细配置说明
├── requirements.txt             # Python 依赖
├── .env.example                 # 环境变量示例
├── .gitignore                   # Git 忽略文件
├── main.py                      # 主程序入口
│
├── config/                      # 配置文件
│   └── config.py               # 系统配置（邮件、市场、分析参数）
│
├── src/                         # 源代码目录
│   ├── __init__.py
│   │
│   ├── data_sources/           # 数据源配置
│   │   ├── __init__.py
│   │   └── sources.py         # 数据源定义（AKShare、yFinance）
│   │
│   ├── fetchers/               # 数据获取模块
│   │   ├── __init__.py
│   │   ├── china_fetcher.py    # A股数据获取器
│   │   ├── hk_fetcher.py       # 港股数据获取器
│   │   └── us_fetcher.py       # 美股数据获取器
│   │
│   ├── analyzers/              # 分析引擎
│   │   ├── __init__.py
│   │   ├── fundamental_analyzer.py           # 基本面分析
│   │   ├── technical_analyzer.py             # 技术面分析（基础）
│   │   └── advanced_technical_analyzer.py    # 技术面分析（高级）
│   │
│   ├── recommenders/           # 投资建议模块
│   │   ├── __init__.py
│   │   └── recommender.py     # 投资建议生成器
│   │
│   ├── reporters/              # 报告生成模块
│   │   ├── __init__.py
│   │   └── report_generator.py # HTML 报告生成器
│   │
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       └── email_sender.py    # 邮件发送器
│
├── .github/                    # GitHub Actions 配置
│   └── workflows/
│       └── daily-report.yml    # 每日报告定时任务
│
└── reports/                    # 报告输出目录（运行时生成）
    └── report_YYYYMMDD_HHMMSS.html
```

## 模块说明

### 1. 主程序 (main.py)

- `InvestmentAdvisor` 类：核心控制器
  - `fetch_china_data()` - 获取中国股市数据
  - `fetch_hk_data()` - 获取港股数据
  - `fetch_us_data()` - 获取美股数据
  - `analyze_stocks()` - 分析股票
  - `generate_report()` - 生成报告
  - `send_email_report()` - 发送邮件
  - `run()` - 执行完整流程

### 2. 数据获取模块 (src/fetchers/)

#### ChinaStockFetcher
- `get_index_data()` - 获取指数数据
- `get_all_stocks()` - 获取所有 A 股列表
- `get_stock_data()` - 获取个股历史数据
- `get_hot_stocks()` - 获取热门股票
- `get_hot_sectors()` - 获取热门板块
- `get_sector_stocks()` - 获取板块内的股票

#### HongKongStockFetcher
- `get_index_data()` - 获取港股指数数据
- `get_stock_data()` - 获取港股数据
- `get_all_stocks()` - 获取所有港股列表
- `get_hot_stocks()` - 获取热门港股

#### USStockFetcher
- `get_index_data()` - 获取美股指数数据
- `get_stock_data()` - 获取美股数据
- `get_stock_info()` - 获取股票基本信息
- `get_hot_stocks()` - 获取热门美股
- `get_sector_performance()` - 获取板块表现

### 3. 分析引擎 (src/analyzers/)

#### FundamentalAnalyzer（基本面分析）
- `analyze_stock()` - 分析个股基本面
  - PE 评分
  - PB 评分
  - ROE 评分
  - 营收增长评分
  - 利润增长评分
- `analyze_market()` - 分析市场整体基本面

#### AdvancedTechnicalAnalyzer（技术面分析）
- **趋势指标**：
  - 移动平均线 (MA)：5日、10日、20日、40日、60日、120日
  - 指数移动平均线 (EMA)：12日、26日

- **动量指标**：
  - RSI (相对强弱指标)
  - MACD (指数平滑异同移动平均线)
  - Stochastic (随机指标)
  - Williams %R (威廉指标)
  - Momentum (动量指标)
  - ROC (变化率)

- **波动率指标**：
  - Bollinger Bands (布林带)
  - ATR (平均真实波幅)
  - CCI (商品通道指标)

- **成交量指标**：
  - OBV (能量潮指标)
  - Volume Ratio (量比)
  - VWAP (成交量加权平均价)

- **支撑阻力**：
  - Fibonacci Retracement (斐波那契回调)
  - 支撑阻力位检测

- **综合分析**：
  - `analyze_trend()` - 趋势分析
  - `analyze_momentum()` - 动量分析
  - `analyze_volume()` - 成交量分析
  - `analyze_volatility()` - 波动率分析
  - `generate_comprehensive_signal()` - 生成综合信号

### 4. 投资建议模块 (src/recommenders/)

#### Recommender
- `generate_recommendation()` - 生成单只股票的投资建议
  - 综合评分计算
  - 评级（强烈推荐/推荐/观望/中性/不推荐）
  - 操作建议
  - 目标价格
  - 止损价格
  - 风险等级
  - 持有周期
  - 推荐理由

- `select_top_stocks()` - 筛选最佳投资标的
- `generate_portfolio_suggestion()` - 生成投资组合建议

### 5. 报告生成模块 (src/reporters/)

#### ReportGenerator
- `generate_html_report()` - 生成 HTML 格式报告
  - 市场概况
  - 热门股票列表
  - 板块表现
  - 投资建议
  - 风险提示
- `save_report()` - 保存报告到文件

### 6. 工具模块 (src/utils/)

#### EmailSender
- `send_email()` - 发送邮件
- `send_investment_report()` - 发送投资报告

## 工作流程

```
开始
  ↓
获取三大市场数据（A股、港股、美股）
  ↓
筛选热门股票（涨幅榜、成交量榜）
  ↓
基本面分析（PE、PB、ROE、增长等）
  ↓
技术面分析（多指标综合评分）
  ├─ 趋势分析（短期、中期、长期）
  ├─ 动量分析（RSI、MACD等）
  ├─ 成交量分析（OBV、量比）
  └─ 波动率分析（布林带、ATR）
  ↓
生成投资建议（综合评分、买卖点、目标价、止损价）
  ↓
生成 HTML 报告
  ↓
发送邮件到 QQ 邮箱
  ↓
完成
```

## 数据流

```
数据源 (AKShare/yFinance)
  ↓
Fetchers (数据获取器)
  ↓
Analyzers (分析引擎)
  ├─ FundamentalAnalyzer (基本面)
  └─ AdvancedTechnicalAnalyzer (技术面)
  ↓
Recommender (投资建议生成)
  ↓
ReportGenerator (报告生成)
  ↓
EmailSender (邮件发送)
  ↓
用户 (接收报告)
```

## 配置说明

### 环境变量 (.env)
- 邮箱配置（SMTP服务器、端口、发件人、密码）
- 收件人邮箱
- OpenAI API 密钥（可选）

### 系统配置 (config/config.py)
- 邮件配置
- 市场配置（指数、板块）
- 分析参数（均线周期、RSI周期等）
- 推荐阈值

### GitHub Actions 配置
- 定时任务 (cron 表达式)
- 环境变量 (Secrets)
- 工作流程定义

## 扩展指南

### 添加新的技术指标

在 `src/analyzers/advanced_technical_analyzer.py` 中添加新的计算方法。

### 添加新的数据源

在 `src/fetchers/` 中创建新的 Fetcher 类，继承基本功能。

### 自定义报告模板

修改 `src/reporters/report_generator.py` 中的 HTML 模板。

### 调整定时策略

修改 `.github/workflows/daily-report.yml` 中的 cron 表达式。

## 依赖项

- **数据获取**：akshare、yfinance
- **数据分析**：pandas、numpy、scipy
- **技术分析**：TA-Lib
- **报告生成**：jinja2
- **邮件发送**：smtplib
- **配置管理**：python-dotenv
- **任务调度**：schedule

## 性能考虑

- 数据获取添加了延时，避免被限制
- 只分析热门股票的前20只，避免处理过多数据
- 使用缓存机制可以进一步优化
- 异步处理可以提高效率

## 安全考虑

- 敏感信息使用环境变量和 GitHub Secrets
- .env 文件已在 .gitignore 中
- 不在代码中硬编码密码和密钥
- 邮件授权码定期更换建议
