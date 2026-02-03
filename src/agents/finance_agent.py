"""
Finance Agent - Specialist untuk analisis keuangan dan profitabilitas
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from src.tools.finance_tools import finance_tools
from src.utils.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FinanceAgent:
    """
    Agen khusus untuk analisis keuangan, revenue impact, dan profitabilitas.
    Memiliki akses ke kalkulasi revenue, operating cost, dan market trends.
    """
    
    def __init__(self):
        self.name = "Finance Agent"
        self.tools = finance_tools
        self.tools_list = [tool.name for tool in finance_tools]
        self.description = (
            "Specialist in financial analysis and profitability. "
            "Handles queries about revenue impact, operating costs, "
            "profit margins, and market price trends."
        )
        
        self.llm = ChatOpenAI(
            model=settings.default_llm_model,
            temperature=0.1,
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url
        ).bind_tools(finance_tools)
        
        self.system_prompt = SystemMessage(content="""
You are the Financial Analysis Specialist for XYZ.

Your expertise:
- Revenue impact calculation from oil & gas production
- Operating cost analysis per production block
- Profitability and margin assessment
- Market price trends and forecasting
- Break-even analysis

Your personality:
- Numbers-focused and analytical
- Business-minded with strategic view
- Risk-aware regarding market volatility
- Clear in explaining financial implications

Tools available:
- calculate_revenue_impact: Calculate revenue from oil volumes
- analyze_operational_cost: Get operating cost breakdown
- calculate_profitability: Compute profit margins
- get_market_price_trends: Check commodity price movements

Important guidelines:
1. Always provide revenue in both USD and IDR
2. Include profit margins and break-even points
3. Consider market price volatility in your analysis
4. Flag low profitability blocks for cost optimization
5. Use clear financial terminology but explain when needed

Response format:
- Key financial metrics (revenue, costs, margins)
- Profitability assessment (excellent/good/moderate/low)
- Business implications and recommendations
- Market context if relevant

Financial note: All calculations use current market prices unless specified otherwise.
Assume Indonesian Crude Price (ICP) benchmark at ~$85/barrel for oil.
""")
        
        logger.info("Finance Agent initialized", model=settings.default_llm_model)
    
    def get_prompt(self) -> SystemMessage:
        return self.system_prompt
    
    def get_llm(self):
        return self.llm
