# 自动投资顾问系统 - 配置说明

## 环境配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置邮箱

你需要配置 QQ 邮箱作为发件人：

1. 登录 QQ 邮箱
2. 进入"设置" -> "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"IMAP/SMTP服务"
5. 生成授权码（不是QQ密码，是专门用于SMTP的授权码）

### 3. 配置 .env 文件

复制 `.env.example` 到 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的配置：

```env
EMAIL_SMTP_SERVER=smtp.qq.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=your_qq@qq.com
EMAIL_PASSWORD=your_qq_authorization_code
EMAIL_RECEIVER=receiver@qq.com

OPENAI_API_KEY=your_openai_api_key
```

**重要说明：**
- `EMAIL_SENDER`: 你的 QQ 邮箱地址
- `EMAIL_PASSWORD`: 你的 QQ 邮箱授权码（不是QQ登录密码）
- `EMAIL_RECEIVER`: 接收报告的邮箱地址
- `OPENAI_API_KEY`: OpenAI API 密钥（如果需要使用AI分析）

## GitHub Actions 配置

### 1. 创建 GitHub 仓库

```bash
cd auto-investment-advisor
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/auto-investment-advisor.git
git push -u origin main
```

### 2. 配置 GitHub Secrets

在 GitHub 仓库中配置 Secrets：

1. 进入仓库的 Settings -> Secrets and variables -> Actions
2. 点击 "New repository secret"
3. 添加以下 Secrets：

| Name | Value | Description |
|------|-------|-------------|
| `EMAIL_SMTP_SERVER` | `smtp.qq.com` | SMTP 服务器地址 |
| `EMAIL_SMTP_PORT` | `587` | SMTP 端口 |
| `EMAIL_SENDER` | `your_qq@qq.com` | 发件人邮箱 |
| `EMAIL_PASSWORD` | `your_authorization_code` | QQ 邮箱授权码 |
| `EMAIL_RECEIVER` | `receiver@qq.com` | 收件人邮箱 |
| `OPENAI_API_KEY` | `sk-...` | OpenAI API 密钥（可选） |

### 3. 定时任务配置

`.github/workflows/daily-report.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 8 * * *'
```

这表示每天北京时间 16:00（UTC 8:00）执行。

Cron 表达式格式：`分 时 日 月 周`

常用配置：
- 每天早上 9 点：`0 1 * * *`（UTC 时间）
- 每天下午 3 点：`0 7 * * *`（UTC 时间）
- 工作日早上 9 点：`0 1 * * 1-5`（UTC 时间）

### 4. 手动触发

如果你想手动触发任务：

1. 进入 GitHub 仓库的 Actions 标签
2. 选择 "Investment Advisor Daily Report" workflow
3. 点击 "Run workflow" 按钮

## 本地运行

### 运行完整流程

```bash
python main.py
```

### 单独测试模块

```python
# 测试中国股市数据获取
from src.fetchers.china_fetcher import ChinaStockFetcher
fetcher = ChinaStockFetcher()
hot_stocks = fetcher.get_hot_stocks()
print(hot_stocks)

# 测试技术分析
from src.analyzers.advanced_technical_analyzer import AdvancedTechnicalAnalyzer
analyzer = AdvancedTechnicalAnalyzer()
# 需要传入历史数据
```

## 常见问题

### 1. 邮件发送失败

- 检查邮箱授权码是否正确
- 确认已开启 SMTP 服务
- 检查网络连接

### 2. 数据获取失败

- 检查网络连接
- 可能遇到 API 限制，程序已内置延时
- 某些数据源可能临时不可用

### 3. GitHub Actions 执行失败

- 检查 Secrets 是否正确配置
- 查看 Actions 日志获取详细错误信息
- 确认依赖项是否正确安装

### 4. QQ 邮箱限制

- 每日发送邮件数量有限制
- 避免频繁发送大量邮件
- 遵守 QQ 邮箱使用条款

## 性能优化建议

1. **数据缓存**：可以添加本地缓存机制，减少重复请求
2. **异步处理**：使用异步IO提高数据获取效率
3. **批量处理**：合理安排批量获取数据的数量
4. **错误重试**：添加自动重试机制处理临时网络问题

## 安全建议

1. **不要提交 .env 文件**：已在 .gitignore 中排除
2. **使用 GitHub Secrets**：敏感信息不要直接写在代码中
3. **定期更新密钥**：定期更换授权码和 API 密钥
4. **限制访问权限**：合理配置仓库访问权限

## 数据源说明

### 中国股市数据
- 使用 akshare 接口
- 包含实时行情、历史数据、板块信息
- 已添加请求间隔，避免被限制

### 港股数据
- 使用 yfinance 和 akshare
- 获取港股指数和个股数据
- 注意港股和 A 股的代码格式差异

### 美股数据
- 使用 yfinance
- 获取美股指数、个股和板块数据
- 注意时区差异

## 技术分析指标

系统使用多种技术分析指标：

1. **趋势指标**：MA (移动平均线)、EMA (指数移动平均线)
2. **动量指标**：RSI、MACD、Stochastic、Williams %R
3. **波动率指标**：Bollinger Bands、ATR
4. **成交量指标**：OBV、Volume Ratio
5. **支撑阻力**：Fibonacci Retracement

每个指标都会给出评分，综合计算总分。

## 风险提示

1. 本系统仅供参考，不构成投资建议
2. 股市有风险，投资需谨慎
3. 历史表现不代表未来收益
4. 建议结合其他分析方法和市场环境综合判断
5. 设置合理的止损点，控制风险

## 许可证

MIT License
