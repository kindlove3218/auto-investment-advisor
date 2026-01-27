# 自动投资顾问系统

每天自动获取中国股市、港股、美股投资机会和热点，并生成详细的投资分析报告。

## 功能特性

- 📊 自动获取三大市场（A股、港股、美股）数据
- 🔍 热点板块和个股分析
- 📈 基本面和技术面分析
- 💡 具体的投资建议（买卖点、价格目标）
- 📧 每日邮件推送
- ⏰ GitHub Actions 自动定时执行

## 项目结构

```
auto-investment-advisor/
├── src/
│   ├── data_sources/      # 数据源配置
│   ├── fetchers/          # 数据获取
│   ├── analyzers/         # 分析引擎
│   ├── recommenders/      # 投资建议
│   ├── reporters/         # 报告生成
│   └── utils/             # 工具函数
├── config/                # 配置文件
├── .github/               # GitHub Actions
└── main.py               # 主程序入口
```

## 安装

```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env.example` 到 `.env`
2. 填入必要的配置信息（邮箱 API 密钥等）

## 运行

```bash
python main.py
```

## 许可证

MIT License
