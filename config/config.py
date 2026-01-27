import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_CONFIG = {
    "smtp_server": os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("EMAIL_SMTP_PORT", 587)),
    "sender": os.getenv("EMAIL_SENDER"),
    "password": os.getenv("EMAIL_PASSWORD"),
    "receiver": os.getenv("EMAIL_RECEIVER")
}

MARKETS = {
    "cn": {
        "name": "中国股市",
        "indices": ["000001.SH", "399001.SZ", "000300.SH"],
        "hot_sectors": []
    },
    "hk": {
        "name": "港股",
        "indices": ["^HSI", "^HSCEI"],
        "hot_sectors": []
    },
    "us": {
        "name": "美股",
        "indices": ["^GSPC", "^DJI", "^IXIC"],
        "hot_sectors": []
    }
}

ANALYSIS_CONFIG = {
    "short_ma": [5, 10],
    "long_ma": [20, 60],
    "rsi_period": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9
}

RECOMMENDATION_CONFIG = {
    "buy_threshold": 0.7,
    "sell_threshold": 0.3,
    "min_score": 60
}
