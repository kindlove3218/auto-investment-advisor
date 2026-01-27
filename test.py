"""
测试脚本 - 用于验证各个模块是否正常工作
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.fetchers.china_fetcher import ChinaStockFetcher
from src.fetchers.hk_fetcher import HongKongStockFetcher
from src.fetchers.us_fetcher import USStockFetcher
from src.analyzers.fundamental_analyzer import FundamentalAnalyzer
from src.analyzers.advanced_technical_analyzer import AdvancedTechnicalAnalyzer
from src.recommenders.recommender import Recommender
from src.reporters.report_generator import ReportGenerator
from src.utils.email_sender import EmailSender
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_china_fetcher():
    print("\n" + "="*50)
    print("测试中国股市数据获取")
    print("="*50)
    
    try:
        fetcher = ChinaStockFetcher()
        
        print("1. 获取热门股票...")
        hot_stocks = fetcher.get_hot_stocks()
        print(f"   获取到 {len(hot_stocks.get('top_gainers', []))} 只涨幅榜股票")
        if not hot_stocks.get('top_gainers').empty:
            print("   示例数据：")
            print(hot_stocks['top_gainers'].head(3))
        
        print("\n2. 获取热门板块...")
        hot_sectors = fetcher.get_hot_sectors()
        print(f"   获取到 {len(hot_sectors)} 个热门板块")
        if not hot_sectors.empty:
            print("   示例数据：")
            print(hot_sectors.head(3))
        
        print("\n✓ 中国股市数据获取测试通过")
        return True
        
    except Exception as e:
        print(f"\n✗ 中国股市数据获取测试失败: {e}")
        return False


def test_hk_fetcher():
    print("\n" + "="*50)
    print("测试港股数据获取")
    print("="*50)
    
    try:
        fetcher = HongKongStockFetcher()
        
        print("1. 获取热门股票...")
        hot_stocks = fetcher.get_hot_stocks()
        print(f"   获取到 {len(hot_stocks.get('top_gainers', []))} 只涨幅榜股票")
        if not hot_stocks.get('top_gainers').empty:
            print("   示例数据：")
            print(hot_stocks['top_gainers'].head(3))
        
        print("\n✓ 港股数据获取测试通过")
        return True
        
    except Exception as e:
        print(f"\n✗ 港股数据获取测试失败: {e}")
        return False


def test_us_fetcher():
    print("\n" + "="*50)
    print("测试美股数据获取")
    print("="*50)
    
    try:
        fetcher = USStockFetcher()
        
        print("1. 获取热门股票...")
        hot_stocks = fetcher.get_hot_stocks()
        print(f"   获取到 {len(hot_stocks)} 只热门股票")
        if not hot_stocks.empty:
            print("   示例数据：")
            print(hot_stocks.head(3))
        
        print("\n2. 获取板块表现...")
        sectors = fetcher.get_sector_performance()
        print(f"   获取到 {len(sectors)} 个板块")
        if not sectors.empty:
            print("   示例数据：")
            print(sectors.head(3))
        
        print("\n✓ 美股数据获取测试通过")
        return True
        
    except Exception as e:
        print(f"\n✗ 美股数据获取测试失败: {e}")
        return False


def test_technical_analyzer():
    print("\n" + "="*50)
    print("测试技术分析")
    print("="*50)
    
    try:
        analyzer = AdvancedTechnicalAnalyzer()
        
        print("1. 创建测试数据...")
        import pandas as pd
        import numpy as np
        np.random.seed(42)
        
        dates = pd.date_range(start='2023-01-01', periods=200, freq='D')
        data = {
            'Open': np.random.randn(200).cumsum() + 100,
            'High': np.random.randn(200).cumsum() + 102,
            'Low': np.random.randn(200).cumsum() + 98,
            'Close': np.random.randn(200).cumsum() + 100,
            'Volume': np.random.randint(1000000, 10000000, 200)
        }
        df = pd.DataFrame(data, index=dates)
        df['High'] = df[['Open', 'Close']].max(axis=1) + np.random.rand(200)
        df['Low'] = df[['Open', 'Close']].min(axis=1) - np.random.rand(200)
        
        print("2. 执行技术分析...")
        analysis = analyzer.generate_comprehensive_signal(df)
        
        if analysis:
            print(f"   综合信号: {analysis['overall_signal']}")
            print(f"   操作建议: {analysis['action']}")
            print(f"   总评分: {analysis['total_score']}")
            print(f"   趋势: {analysis['trend']['trend']}")
            print(f"   动量: {analysis['momentum']['momentum']}")
            print(f"   成交量: {analysis['volume']['volume']}")
            print(f"   波动率: {analysis['volatility']['volatility']}")
            
            print("\n✓ 技术分析测试通过")
            return True
        else:
            print("\n✗ 技术分析测试失败: 未返回分析结果")
            return False
        
    except Exception as e:
        print(f"\n✗ 技术分析测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_recommender():
    print("\n" + "="*50)
    print("测试投资建议生成")
    print("="*50)
    
    try:
        recommender = Recommender()
        
        fundamental_analysis = {
            'total_score': 75,
            'pe_score': '合理',
            'pb_score': '合理',
            'roe_score': '优秀',
            'revenue_growth_score': '良好',
            'profit_growth_score': '良好'
        }
        
        technical_analysis = {
            'total_score': 70,
            'trend': {'trend': '强势上升'},
            'momentum': {'momentum': '向上'},
            'volume': {'volume': '良好'},
            'current_data': {
                'price': 100.0,
                'atr': 5.0
            },
            'support_resistance': {
                'nearest_resistance': 115.0,
                'nearest_support': 90.0
            }
        }
        
        recommendation = recommender.generate_recommendation(
            stock_code='600000',
            stock_name='浦发银行',
            fundamental_analysis=fundamental_analysis,
            technical_analysis=technical_analysis
        )
        
        print("   股票代码:", recommendation['code'])
        print("   股票名称:", recommendation['name'])
        print("   基本面评分:", recommendation['fundamental_score'])
        print("   技术面评分:", recommendation['technical_score'])
        print("   综合评分:", recommendation['total_score'])
        print("   评级:", recommendation['rating'])
        print("   操作建议:", recommendation['action'])
        print("   目标价格:", recommendation['target_price'])
        print("   止损价格:", recommendation['stop_loss'])
        print("   风险等级:", recommendation['risk_level'])
        print("   推荐理由:", recommendation['reasons'])
        
        print("\n✓ 投资建议生成测试通过")
        return True
        
    except Exception as e:
        print(f"\n✗ 投资建议生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_report_generator():
    print("\n" + "="*50)
    print("测试报告生成")
    print("="*50)
    
    try:
        generator = ReportGenerator()
        
        cn_data = {
            'hot_stocks': {
                'top_gainers': pd.DataFrame([
                    {'代码': '600000', '名称': '浦发银行', '涨跌幅': 5.0},
                    {'代码': '600036', '名称': '招商银行', '涨跌幅': 4.5}
                ])
            },
            'hot_sectors': pd.DataFrame([
                {'板块名称': '银行', '涨跌幅': 3.5, '最新价': 100.0}
            ])
        }
        
        hk_data = {}
        us_data = {}
        
        recommendations = [
            {
                'code': '600000',
                'name': '浦发银行',
                'rating': '强烈推荐',
                'action': '建议买入',
                'total_score': 80,
                'current_price': 100.0,
                'target_price': 115.0,
                'stop_loss': 90.0,
                'risk_level': '低',
                'reasons': ['估值合理', 'ROE优秀']
            }
        ]
        
        html_content = generator.generate_html_report(cn_data, hk_data, us_data, recommendations)
        
        if html_content:
            print("   HTML 报告生成成功")
            print(f"   报告长度: {len(html_content)} 字符")
            
            filepath = generator.save_report(html_content)
            print(f"   报告已保存: {filepath}")
            
            print("\n✓ 报告生成测试通过")
            return True
        else:
            print("\n✗ 报告生成测试失败: 未生成内容")
            return False
        
    except Exception as e:
        print(f"\n✗ 报告生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_email_sender():
    print("\n" + "="*50)
    print("测试邮件发送")
    print("="*50)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    email_config = {
        'smtp_server': os.getenv('EMAIL_SMTP_SERVER'),
        'smtp_port': int(os.getenv('EMAIL_SMTP_PORT', 587)),
        'sender': os.getenv('EMAIL_SENDER'),
        'password': os.getenv('EMAIL_PASSWORD'),
        'receiver': os.getenv('EMAIL_RECEIVER')
    }
    
    if not all([email_config['sender'], email_config['password'], email_config['receiver']]):
        print("   邮件配置不完整，跳过邮件发送测试")
        print("   请在 .env 文件中配置 EMAIL_SENDER、EMAIL_PASSWORD 和 EMAIL_RECEIVER")
        return True
    
    try:
        sender = EmailSender(
            smtp_server=email_config['smtp_server'],
            smtp_port=email_config['smtp_port'],
            sender=email_config['sender'],
            password=email_config['password']
        )
        
        test_subject = "【测试】投资顾问系统邮件发送测试"
        test_body = """
        <h1>这是一封测试邮件</h1>
        <p>如果您收到这封邮件，说明邮件发送功能正常。</p>
        <p>投资顾问系统已准备就绪！</p>
        """
        
        print(f"   发件人: {email_config['sender']}")
        print(f"   收件人: {email_config['receiver']}")
        
        success = sender.send_email(
            receiver=email_config['receiver'],
            subject=test_subject,
            body=test_body,
            html=True
        )
        
        if success:
            print("\n✓ 邮件发送测试通过")
            return True
        else:
            print("\n✗ 邮件发送测试失败")
            return False
        
    except Exception as e:
        print(f"\n✗ 邮件发送测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*60)
    print("          投资顾问系统 - 模块测试")
    print("="*60)
    
    results = {}
    
    results['中国股市数据获取'] = test_china_fetcher()
    results['港股数据获取'] = test_hk_fetcher()
    results['美股数据获取'] = test_us_fetcher()
    results['技术分析'] = test_technical_analyzer()
    results['投资建议生成'] = test_recommender()
    results['报告生成'] = test_report_generator()
    results['邮件发送'] = test_email_sender()
    
    print("\n" + "="*60)
    print("          测试总结")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name:20s} {status}")
    
    print("\n" + "-"*60)
    print(f"总计: {passed}/{total} 项测试通过")
    print("="*60)
    
    if passed == total:
        print("\n🎉 所有测试通过！系统已准备就绪。")
        print("\n下一步:")
        print("1. 运行 'python main.py' 执行完整流程")
        print("2. 配置 GitHub Secrets 并部署")
    else:
        print("\n⚠️  部分测试失败，请检查配置和依赖。")


if __name__ == "__main__":
    main()
