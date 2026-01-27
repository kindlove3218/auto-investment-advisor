# 快速开始指南

## 第一步：安装依赖

```bash
cd auto-investment-advisor
pip install -r requirements.txt
```

## 第二步：配置邮箱

1. 获取 QQ 邮箱授权码：
   - 登录 QQ 邮箱 -> 设置 -> 账户
   - 开启 IMAP/SMTP 服务
   - 生成授权码

2. 配置 `.env` 文件：

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
```

## 第三步：测试运行

```bash
python main.py
```

如果配置正确，你应该看到：
1. 程序开始获取三大市场的数据
2. 进行技术分析
3. 生成 HTML 报告
4. 发送邮件到你的邮箱

## 第四步：部署到 GitHub

### 1. 初始化 Git 仓库

```bash
git init
git add .
git commit -m "Initial commit"
```

### 2. 创建 GitHub 仓库

在 GitHub 上创建一个新仓库，然后：

```bash
git remote add origin https://github.com/your-username/auto-investment-advisor.git
git branch -M main
git push -u origin main
```

### 3. 配置 Secrets

在 GitHub 仓库中添加 Secrets：

Settings -> Secrets and variables -> Actions -> New repository secret

添加以下 Secrets：
- `EMAIL_SMTP_SERVER` = `smtp.qq.com`
- `EMAIL_SMTP_PORT` = `587`
- `EMAIL_SENDER` = `your_qq@qq.com`
- `EMAIL_PASSWORD` = `your_qq_authorization_code`
- `EMAIL_RECEIVER` = `receiver@qq.com`
- `OPENAI_API_KEY` = `your_openai_api_key`（可选）

### 4. 手动触发测试

1. 进入 Actions 标签
2. 选择 "Investment Advisor Daily Report"
3. 点击 "Run workflow"

### 5. 确认定时任务

`.github/workflows/daily-report.yml` 已配置为每天 UTC 8:00（北京时间 16:00）运行。

如需修改时间，编辑 cron 表达式：

```yaml
schedule:
  - cron: '0 8 * * *'  # 每天北京时间 16:00
```

## 常见问题解决

### 邮件发送失败

1. 检查授权码是否正确
2. 确认 SMTP 服务已开启
3. 测试网络连接

### 数据获取失败

1. 检查网络连接
2. 某些数据源可能临时不可用
3. 程序已内置延时，避免被限制

### GitHub Actions 执行失败

1. 检查 Secrets 是否正确
2. 查看 Actions 日志
3. 确认依赖项安装成功

## 功能说明

### 技术分析指标

系统使用多种先进技术分析指标：

1. **趋势分析**：短期、中期、长期移动平均线
2. **动量指标**：RSI、MACD、Stochastic、Williams %R
3. **波动率指标**：Bollinger Bands、ATR
4. **成交量分析**：OBV、Volume Ratio
5. **支撑阻力**：Fibonacci Retracement
6. **综合评分**：多指标加权评分

### 投资建议

根据综合评分给出：
- **强烈推荐** (80-100分)：建议买入，低风险
- **推荐** (70-79分)：建议买入，中低风险
- **观望** (60-69分)：逢低关注，中等风险
- **中性** (50-59分)：谨慎持有，中等偏高风险
- **不推荐** (0-49分)：建议规避，高风险

### 报告内容

每日报告包含：
- 🇨🇳 中国股市：涨幅榜、热门板块
- 🇭🇰 港股市场：涨幅榜
- 🇺🇸 美股市场：热门股票、板块表现
- 💡 投资建议：前10名推荐股票的详细分析
- 📋 市场总结和风险提示

## 下一步

1. **自定义分析**：修改 `src/analyzers/` 中的参数
2. **调整报告模板**：编辑 `src/reporters/report_generator.py`
3. **添加更多数据源**：扩展 `src/fetchers/` 中的数据获取器
4. **优化定时策略**：调整 `.github/workflows/daily-report.yml` 中的 cron 表达式

## 获取帮助

- 查看 `README.md` 了解项目概览
- 查看 `SETUP.md` 了解详细配置说明
- 查看代码注释了解具体实现

## 免责声明

本系统仅供参考，不构成投资建议。股市有风险，投资需谨慎。
