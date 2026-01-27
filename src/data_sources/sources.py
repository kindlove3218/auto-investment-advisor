DATA_SOURCES = {
    "cn": {
        "akshare": {
            "enabled": True,
            "functions": {
                "index_data": "ak.stock_zh_index_daily",
                "stock_list": "ak.stock_zh_a_spot_em",
                "hot_stocks": "ak.stock_zh_a_spot_em"
            }
        }
    },
    "hk": {
        "yfinance": {
            "enabled": True,
            "functions": {
                "stock_data": "yf.download",
                "index_data": "yf.download"
            }
        },
        "akshare": {
            "enabled": True,
            "functions": {
                "stock_list": "ak.stock_hk_spot_em",
                "hot_stocks": "ak.stock_hk_spot_em"
            }
        }
    },
    "us": {
        "yfinance": {
            "enabled": True,
            "functions": {
                "stock_data": "yf.download",
                "index_data": "yf.download"
            }
        }
    }
}

MARKET_NEWS_SOURCES = {
    "cn": [
        "https://finance.eastmoney.com/a/jzx.html",
        "https://finance.sina.com.cn/stock/"
    ],
    "hk": [
        "https://www.aastocks.com/tc/news/market/",
        "https://www.etnet.com.hk/news/latest"
    ],
    "us": [
        "https://finance.yahoo.com/",
        "https://www.bloomberg.com/markets"
    ]
}
