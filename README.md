# 自动投资顾问系统

每天自动获取中国股市、港股、美股投资机会和热点，并生成详细的投资分析报告。

## 功能特性

- 📊 自动获取三大市场（A股、港股、美股）数据
- 🔍 热点板块和个股分析
- 📈 基本面和技术面分析（10+ 种高级指标）
- 💡 具体的投资建议（买卖点、价格目标、止损价）
- 📧 每日邮件推送
- ⏰ GitHub Actions 自动定时执行
- 🧩 模块化设计，灵活运行

## 项目架构

### 模块化设计

系统分为两个独立模块：

#### 1. 数据获取模块 (`fetch_data.py`)
- 获取三大市场的实时数据
- 收集热门股票和板块信息
- 保存为 JSON 文件

#### 2. 股票分析模块 (`analyze_stocks.py`)
- 加载市场数据
- 进行基本面和技术面分析
- 生成投资建议和 HTML 报告
- 发送邮件推送

详见 [ARCHITECTURE_NEW.md](ARCHITECTURE_NEW.md)

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境

1. 复制 `.env.example` 到 `.env`
2. 配置 QQ 邮箱授权码和收件人

```bash
cp .env.example .env
```

编辑 `.env`：

```env
EMAIL_SMTP_SERVER=smtp.qq.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=your_qq@qq.com
EMAIL_PASSWORD=your_qq_authorization_code
EMAIL_RECEIVER=receiver@qq.com
OPENAI_API_KEY=your_openai_api_key
RUN_MODE=full
```

### 运行方式

#### 方式 1：完整流程

```bash
python main.py
```

#### 方式 2：只获取数据

```bash
python fetch_data.py
# 或
RUN_MODE=fetch python main.py
```

#### 方式 3：只分析股票

```bash
python analyze_stocks.py
# 或指定数据文件
python analyze_stocks.py data/market_data_20240127_160000.json
# 或
RUN_MODE=analyze python main.py
```

## 部署到 GitHub

### 1. 创建 GitHub 仓库

访问 https://github.com/new 创建仓库。

### 2. 推送代码

```bash
git remote add origin https://github.com/your-username/auto-investment-advisor.git
git branch -M main
git push -u origin main
```

### 3. 配置 GitHub Secrets

在仓库 Settings -> Secrets and variables -> Actions 中添加：

| Name | Value |
|------|-------|
| `EMAIL_SMTP_SERVER` | `smtp.qq.com` |
| `EMAIL_SMTP_PORT` | `587` |
| `EMAIL_SENDER` | `your_qq@qq.com` |
| `EMAIL_PASSWORD` | `your_qq_authorization_code` |
| `EMAIL_RECEIVER` | `receiver@qq.com` |
| `OPENAI_API_KEY` | `sk-...` (可选) |

### 4. 手动测试

进入 Actions 标签 -> Investment Advisor Daily Report -> Run workflow

### 5. 定时任务

默认每天北京时间 16:00（UTC 8:00）自动执行。

## 项目结构

```
auto-investment-advisor/
├── README.md                      # 项目说明
├── QUICKSTART.md                  # 快速开始指南
├── SETUP.md                       # 详细配置说明
├── ARCHITECTURE_NEW.md            # 架构文档
├── CHANGELOG.md                   # 更新日志
├── LICENSE                        # 许可证
├── requirements.txt                # Python 依赖
├── .env.example                   # 环境变量示例
├── main.py                        # 主程序入口
├── fetch_data.py                  # 数据获取模块
├── analyze_stocks.py              # 股票分析模块
├── test.py                        # 测试脚本
├── config/                        # 配置文件
│   └── config.py
├── src/                           # 源代码
│   ├── data_sources/              # 数据源配置
│   ├── fetchers/                 # 数据获取器
│   ├── analyzers/                # 分析引擎
│   ├── recommenders/             # 投资建议
│   ├── reporters/                # 报告生成
│   └── utils/                   # 工具函数
├── data/                         # 数据存储（不提交）
│   ├── market_data_*.json
│   └── recommendations_*.json
├── reports/                      # 报告输出（不提交）
│   └── report_*.html
└── .github/                      # GitHub Actions
    └── workflows/
        └── daily-report.yml
```

## 技术分析指标

### 趋势指标
- 短期：MA5、MA10
- 中期：MA20、MA40
- 长期：MA60、MA120
- EMA：EMA12、EMA26

### 动量指标
- RSI（相对强弱指标）
- MACD（指数平滑异同移动平均线）
- Stochastic（随机指标）
- Williams %R（威廉指标）
- Momentum（动量指标）
- ROC（变化率）

### 波动率指标
- Bollinger Bands（布林带）
- ATR（平均真实波幅）
- CCI（商品通道指标）

### 成交量指标
- OBV（能量潮指标）
- Volume Ratio（量比）
- VWAP（成交量加权平均价）

### 支撑阻力
- Fibonacci Retracement（斐波那契回调）
- 支撑位检测
- 阻力位检测

## 投资建议

根据综合评分给出五级评级：

| 评级 | 分数 | 操作建议 | 风险等级 |
|------|------|----------|----------|
| 强烈推荐 | 80-100 | 建议买入 | 低 |
| 推荐 | 70-79 | 建议买入 | 中低 |
| 观望 | 60-69 | 逢低关注 | 中等 |
| 中性 | 50-59 | 谨慎持有 | 中等偏高 |
| 不推荐 | 0-49 | 建议规避 | 高 |

每只股票推荐包含：
- 综合评分
- 操作建议
- 目标价格
- 止损价格
- 风险等级
- 持有周期
- 推荐理由

## 文档

- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [SETUP.md](SETUP.md) - 详细配置说明
- [ARCHITECTURE_NEW.md](ARCHITECTURE_NEW.md) - 架构文档
- [ARCHITECTURE.md](ARCHITECTURE.md) - 原架构文档
- [CHANGELOG.md](CHANGELOG.md) - 更新日志

## 测试

```bash
python test.py
```

## 许可证

MIT License

## 免责声明

本系统仅供学习和研究目的使用。任何投资建议仅供参考，不构成投资建议。股市有风险，投资需谨慎。
