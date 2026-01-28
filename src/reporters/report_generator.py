import pandas as pd
from datetime import datetime
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    def __init__(self):
        pass

    def generate_text_report(self, cn_data: Dict, hk_data: Dict, us_data: Dict, 
                          recommendations: List[Dict]) -> str:
        try:
            today = datetime.now().strftime('%Y年%m月%d日')
            
            lines = []
            lines.append("=" * 60)
            lines.append(f"                    股市投资日报")
            lines.append(f"                  {today}")
            lines.append("=" * 60)
            lines.append("")
            
            # 中国股市
            if cn_data and cn_data.get('hot_stocks'):
                lines.append("┌" + "─" * 58 + "┐")
                lines.append("│" + " " * 15 + "🇨🇳 中国股市" + " " * 30 + "│")
                lines.append("└" + "─" * 58 + "┘")
                lines.append("")
                
                if cn_data.get('hot_stocks', {}).get('top_gainers'):
                    lines.append("📈 涨幅榜 TOP 5:")
                    lines.append("-" * 60)
                    for stock in cn_data['hot_stocks']['top_gainers'][:5]:
                        lines.append(f"  {stock.get('代码', ''):8s} {stock.get('名称', ''):10s} "
                                  f"{'↑' if stock.get('涨跌幅', 0) > 0 else '↓'} "
                                  f"{abs(stock.get('涨跌幅', 0)):5.2f}%  "
                                  f"价格: {stock.get('价格', 0):.2f}")
                    lines.append("")
                
                if cn_data.get('hot_sectors'):
                    lines.append("🔥 热门板块 TOP 5:")
                    lines.append("-" * 60)
                    for sector in cn_data['hot_sectors'][:5]:
                        lines.append(f"  {sector.get('板块名称', ''):12s} "
                                  f"{'↑' if sector.get('涨跌幅', 0) > 0 else '↓'} "
                                  f"{abs(sector.get('涨跌幅', 0)):5.2f}%  "
                                  f"上涨: {sector.get('上涨家数', 0):3d}  "
                                  f"下跌: {sector.get('下跌家数', 0):3d}")
                    lines.append("")
            
            # 港股
            if hk_data and hk_data.get('hot_stocks'):
                lines.append("┌" + "─" * 58 + "┐")
                lines.append("│" + " " * 20 + "🇭🇰 港股市场" + " " * 28 + "│")
                lines.append("└" + "─" * 58 + "┘")
                lines.append("")
                
                if hk_data.get('hot_stocks', {}).get('top_gainers'):
                    lines.append("📈 涨幅榜 TOP 5:")
                    lines.append("-" * 60)
                    for stock in hk_data['hot_stocks']['top_gainers'][:5]:
                        lines.append(f"  {stock.get('代码', ''):8s} {stock.get('名称', ''):15s} "
                                  f"{'↑' if stock.get('涨跌幅', 0) > 0 else '↓'} "
                                  f"{abs(stock.get('涨跌幅', 0)):5.2f}%  "
                                  f"价格: {stock.get('价格', 0):.2f}")
                    lines.append("")
            
            # 美股
            if us_data and us_data.get('hot_stocks'):
                lines.append("┌" + "─" * 58 + "┐")
                lines.append("│" + " " * 20 + "🇺🇸 美股市场" + " " * 28 + "│")
                lines.append("└" + "─" * 58 + "┘")
                lines.append("")
                
                if us_data.get('hot_stocks'):
                    lines.append("📈 热门股票 TOP 5:")
                    lines.append("-" * 60)
                    for stock in us_data['hot_stocks'][:5]:
                        lines.append(f"  {stock.get('代码', ''):8s} {stock.get('名称', ''):20s} "
                                  f"{'↑' if stock.get('涨跌幅', 0) > 0 else '↓'} "
                                  f"{abs(stock.get('涨跌幅', 0)):5.2f}%  "
                                  f"价格: {stock.get('价格', 0):.2f}")
                    lines.append("")
                
                if us_data.get('sector_performance'):
                    lines.append("📊 板块表现:")
                    lines.append("-" * 60)
                    for sector in us_data['sector_performance']:
                        lines.append(f"  {sector.get('板块', ''):15s} "
                                  f"{'↑' if sector.get('涨跌幅', 0) > 0 else '↓'} "
                                  f"{abs(sector.get('涨跌幅', 0)):5.2f}%")
                    lines.append("")
            
            # 投资建议
            if recommendations:
                lines.append("┌" + "─" * 58 + "┐")
                lines.append("│" + " " * 18 + "💡 投资建议" + " " * 30 + "│")
                lines.append("└" + "─" * 58 + "┘")
                lines.append("")
                
                for idx, rec in enumerate(recommendations[:10], 1):
                    rating_map = {
                        '强烈推荐': '⭐⭐⭐⭐⭐',
                        '推荐': '⭐⭐⭐⭐',
                        '观望': '⭐⭐',
                        '中性': '⭐',
                        '不推荐': '❌'
                    }
                    rating = rating_map.get(rec.get('rating', ''), '⭐')
                    
                    lines.append(f"【{idx:2d}】{rec.get('name', ''):12s} ({rec.get('code', '')})")
                    lines.append(f"     评级: {rating}  {rec.get('rating', '')}")
                    lines.append(f"     操作: {rec.get('action', '')}")
                    
                    if rec.get('current_price'):
                        lines.append(f"     现价: ¥{rec.get('current_price', 0):.2f}")
                    if rec.get('target_price'):
                        lines.append(f"     目标: ¥{rec.get('target_price', 0):.2f}")
                    if rec.get('stop_loss'):
                        lines.append(f"     止损: ¥{rec.get('stop_loss', 0):.2f}")
                    
                    if rec.get('risk_level'):
                        risk_colors = {
                            '低': '🟢',
                            '中低': '🟢',
                            '中等': '🟡',
                            '中等偏高': '🟠',
                            '高': '🔴'
                        }
                        risk_icon = risk_colors.get(rec.get('risk_level', ''), '⚪')
                        lines.append(f"     风险: {risk_icon} {rec.get('risk_level', '')}")
                    
                    if rec.get('reasons'):
                        lines.append(f"     理由: {', '.join(rec.get('reasons', []))}")
                    
                    lines.append("")
            
            # 风险提示
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 18 + "📋 风险提示" + " " * 30 + "│")
            lines.append("└" + "─" * 58 + "┘")
            lines.append("")
            lines.append("• 本报告基于技术分析和基本面分析，为您精选三大市场的投资机会")
            lines.append("• 请注意，股市有风险，投资需谨慎")
            lines.append("• 建议设置合理的止损点，控制风险")
            lines.append("• 建议分散投资，不要将所有资金投入单一股票")
            lines.append("• 过去的表现不代表未来的收益")
            lines.append("")
            lines.append("=" * 60)
            lines.append("免责声明：投资有风险，入市需谨慎。本报告仅供参考，")
            lines.append("不构成投资建议。请根据个人风险承受能力做出投资决策。")
            lines.append("=" * 60)
            
            text_content = '\n'.join(lines)
            return text_content
        except Exception as e:
            logger.error(f"生成文本报告失败: {e}")
            return ""

    def generate_html_report(self, cn_data: Dict, hk_data: Dict, us_data: Dict, 
                            recommendations: List[Dict]) -> str:
        try:
            today = datetime.now().strftime('%Y年%m月%d日')
            
            template_str = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>股市投资日报 - {{ date }}</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0;
            font-size: 32px;
        }
        .header p {
            margin: 10px 0 0;
            opacity: 0.9;
        }
        .section {
            background: white;
            padding: 25px;
            margin-bottom: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }
        .market-overview {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .market-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .market-card h3 {
            margin-top: 0;
            color: #333;
        }
        .positive {
            color: #28a745;
            font-weight: bold;
        }
        .negative {
            color: #dc3545;
            font-weight: bold;
        }
        .table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        .table th, .table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .table th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        .table tr:hover {
            background-color: #f5f5f5;
        }
        .tag {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 12px;
            margin: 2px;
        }
        .tag-strong-buy {
            background-color: #d4edda;
            color: #155724;
        }
        .tag-buy {
            background-color: #d1ecf1;
            color: #0c5460;
        }
        .tag-hold {
            background-color: #fff3cd;
            color: #856404;
        }
        .tag-sell {
            background-color: #f8d7da;
            color: #721c24;
        }
        .recommendation-card {
            background: #f8f9fa;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .recommendation-card h4 {
            margin: 0 0 10px 0;
            color: #667eea;
        }
        .recommendation-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .detail-item {
            background: white;
            padding: 10px;
            border-radius: 5px;
        }
        .detail-label {
            font-size: 12px;
            color: #666;
        }
        .detail-value {
            font-size: 16px;
            font-weight: bold;
            color: #333;
        }
        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 股市投资日报</h1>
        <p>{{ date }} | 每日精选投资机会分析</p>
    </div>

    {% if cn_data %}
    <div class="section">
        <h2>🇨🇳 中国股市</h2>
        <div class="market-overview">
            {% if cn_data.hot_stocks %}
            <div class="market-card">
                <h3>📈 涨幅榜</h3>
                <table class="table">
                    <thead>
                        <tr>
                            <th>代码</th>
                            <th>名称</th>
                            <th>涨跌幅</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for stock in cn_data.hot_stocks.top_gainers[:5] %}
                        <tr>
                            <td>{{ stock.代码 }}</td>
                            <td>{{ stock.名称 }}</td>
                            <td class="positive">{{ "%.2f"|format(stock.涨跌幅) }}%</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% endif %}
            {% if cn_data.hot_sectors %}
            <div class="market-card">
                <h3>🔥 热门板块</h3>
                <table class="table">
                    <thead>
                        <tr>
                            <th>板块</th>
                            <th>涨跌幅</th>
                            <th>领涨股</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for sector in cn_data.hot_sectors[:5] %}
                        <tr>
                            <td>{{ sector.板块名称 }}</td>
                            <td class="{{ 'positive' if sector.涨跌幅 > 0 else 'negative' }}">
                                {{ "%.2f"|format(sector.涨跌幅) }}%
                            </td>
                            <td>{{ sector.最新价 }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% endif %}
        </div>
    </div>
    {% endif %}

    {% if hk_data %}
    <div class="section">
        <h2>🇭🇰 港股市场</h2>
        <div class="market-overview">
            {% if hk_data.hot_stocks %}
            <div class="market-card">
                <h3>📈 涨幅榜</h3>
                <table class="table">
                    <thead>
                        <tr>
                            <th>代码</th>
                            <th>名称</th>
                            <th>涨跌幅</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for stock in hk_data.hot_stocks.top_gainers[:5] %}
                        <tr>
                            <td>{{ stock.代码 }}</td>
                            <td>{{ stock.名称 }}</td>
                            <td class="positive">{{ "%.2f"|format(stock.涨跌幅) }}%</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% endif %}
        </div>
    </div>
    {% endif %}

    {% if us_data %}
    <div class="section">
        <h2>🇺🇸 美股市场</h2>
        <div class="market-overview">
            {% if us_data.hot_stocks %}
            <div class="market-card">
                <h3>📈 热门股票</h3>
                <table class="table">
                    <thead>
                        <tr>
                            <th>代码</th>
                            <th>名称</th>
                            <th>价格</th>
                            <th>涨跌幅</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for stock in us_data.hot_stocks[:5] %}
                        <tr>
                            <td>{{ stock.代码 }}</td>
                            <td>{{ stock.名称 }}</td>
                            <td>{{ "%.2f"|format(stock.价格) }}</td>
                            <td class="{{ 'positive' if stock.涨跌幅 > 0 else 'negative' }}">
                                {{ "%.2f"|format(stock.涨跌幅) }}%
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% endif %}
            {% if us_data.sector_performance %}
            <div class="market-card">
                <h3>📊 板块表现</h3>
                <table class="table">
                    <thead>
                        <tr>
                            <th>板块</th>
                            <th>涨跌幅</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for sector in us_data.sector_performance %}
                        <tr>
                            <td>{{ sector.板块 }}</td>
                            <td class="{{ 'positive' if sector.涨跌幅 > 0 else 'negative' }}">
                                {{ "%.2f"|format(sector.涨跌幅) }}%
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% endif %}
        </div>
    </div>
    {% endif %}

    <div class="section">
        <h2>💡 投资建议</h2>
        {% if recommendations %}
        {% for rec in recommendations[:10] %}
        <div class="recommendation-card">
            <h4>
                {{ rec.name }} ({{ rec.code }})
                <span class="tag tag-{{ rec.rating }}">{{ rec.rating }}</span>
            </h4>
            <div class="recommendation-details">
                <div class="detail-item">
                    <div class="detail-label">操作建议</div>
                    <div class="detail-value">{{ rec.action }}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">综合评分</div>
                    <div class="detail-value">{{ rec.total_score }}/100</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">当前价格</div>
                    <div class="detail-value">¥{{ rec.current_price }}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">目标价位</div>
                    <div class="detail-value">¥{{ rec.target_price }}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">止损价位</div>
                    <div class="detail-value">¥{{ rec.stop_loss }}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">风险等级</div>
                    <div class="detail-value">{{ rec.risk_level }}</div>
                </div>
            </div>
            {% if rec.reasons %}
            <div style="margin-top: 15px;">
                <strong>推荐理由：</strong>
                {% for reason in rec.reasons %}
                <span class="tag">{{ reason }}</span>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        {% endfor %}
        {% else %}
        <p>暂无推荐股票</p>
        {% endif %}
    </div>

    <div class="section">
        <h2>📋 市场总结</h2>
        <p>本报告基于技术分析和基本面分析，为您精选三大市场的投资机会。请注意，股市有风险，投资需谨慎。</p>
        <p><strong>风险提示：</strong></p>
        <ul>
            <li>本报告仅供参考，不构成投资建议</li>
            <li>投资决策应基于个人风险承受能力和投资目标</li>
            <li>请设置合理的止损点，控制风险</li>
            <li>建议分散投资，不要将所有资金投入单一股票</li>
        </ul>
    </div>

    <div class="footer">
        <p>本报告由自动投资系统生成 | {{ date }}</p>
        <p>免责声明：投资有风险，入市需谨慎。本报告仅供参考，不构成投资建议。</p>
    </div>
</body>
</html>
            """
            
            template = Template(template_str)
            html_content = template.render(
                date=today,
                cn_data=cn_data,
                hk_data=hk_data,
                us_data=us_data,
                recommendations=recommendations
            )
            
            return html_content
        except Exception as e:
            logger.error(f"生成HTML报告失败: {e}")
            return ""

    def save_report(self, content: str, filename: str = None, format: str = 'html') -> str:
        try:
            if not filename:
                filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            
            import os
            if format == 'html':
                os.makedirs('reports', exist_ok=True)
                filepath = f"reports/{filename}"
            else:
                os.makedirs('data', exist_ok=True)
                filepath = f"data/{filename}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"报告已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存报告失败: {e}")
            return ""
