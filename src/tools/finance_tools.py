"""
Tools untuk Finance Agent
Menangani analisis keuangan, revenue, dan profitabilitas
"""
from langchain_core.tools import tool
from typing import Dict, Any
from datetime import datetime, timedelta
import random


@tool
def calculate_revenue_impact(
    oil_volume_barrels: int,
    oil_price_usd: float = 85.0
) -> Dict[str, Any]:
    """
    Menghitung dampak revenue dari produksi atau pengiriman minyak.
    
    Args:
        oil_volume_barrels: Volume minyak dalam barrel
        oil_price_usd: Harga minyak per barrel (default: $85 - ICP estimate)
    
    Returns:
        Dictionary berisi kalkulasi revenue dalam USD dan IDR
    
    Example:
        >>> calculate_revenue_impact(500000, 85.0)
        {
            "volume_barrels": 500000,
            "price_per_barrel_usd": 85.0,
            "total_revenue_usd": 42500000
        }
    """
    # Conversion rate USD to IDR (mock)
    usd_to_idr = 15800
    
    revenue_usd = oil_volume_barrels * oil_price_usd
    revenue_idr = revenue_usd * usd_to_idr
    
    return {
        "volume_barrels": oil_volume_barrels,
        "price_per_barrel_usd": oil_price_usd,
        "total_revenue_usd": round(revenue_usd, 2),
        "total_revenue_idr": round(revenue_idr, 2),
        "exchange_rate": usd_to_idr,
        "calculation_date": datetime.now().strftime("%Y-%m-%d"),
        "price_benchmark": "Indonesian Crude Price (ICP)"
    }


@tool
def analyze_operational_cost(
    block_name: str,
    production_volume_bopd: int
) -> Dict[str, Any]:
    """
    Menganalisis biaya operasional produksi per blok.
    
    Args:
        block_name: Nama blok migas
        production_volume_bopd: Volume produksi dalam BOPD
    
    Returns:
        Dictionary berisi breakdown biaya operasional
    
    Example:
        >>> analyze_operational_cost("Rokan", 150000)
        {
            "block": "Rokan",
            "production_volume_bopd": 150000,
            "operating_cost_per_barrel_usd": 22.5,
            "total_daily_cost_usd": 3375000
        }
    """
    # Mock operating cost per barrel (berbeda per blok)
    cost_per_barrel = {
        "Rokan": 22.5,
        "Mahakam": 28.0,
        "Cepu": 35.0
    }
    
    opex = cost_per_barrel.get(block_name, 25.0)
    daily_cost = production_volume_bopd * opex
    
    # Breakdown cost components
    labor_pct = 0.35
    maintenance_pct = 0.25
    energy_pct = 0.20
    other_pct = 0.20
    
    return {
        "block": block_name,
        "production_volume_bopd": production_volume_bopd,
        "operating_cost_per_barrel_usd": opex,
        "total_daily_cost_usd": round(daily_cost, 2),
        "cost_breakdown": {
            "labor_usd": round(daily_cost * labor_pct, 2),
            "maintenance_usd": round(daily_cost * maintenance_pct, 2),
            "energy_usd": round(daily_cost * energy_pct, 2),
            "other_usd": round(daily_cost * other_pct, 2)
        },
        "analysis_date": datetime.now().strftime("%Y-%m-%d")
    }


@tool
def calculate_profitability(
    revenue_usd: float,
    operating_cost_usd: float
) -> Dict[str, Any]:
    """
    Menghitung metrik profitabilitas dan margin.
    
    Args:
        revenue_usd: Total revenue dalam USD
        operating_cost_usd: Total operating cost dalam USD
    
    Returns:
        Dictionary berisi metrik profitabilitas
    
    Example:
        >>> calculate_profitability(42500000, 3375000)
        {
            "revenue_usd": 42500000,
            "operating_cost_usd": 3375000,
            "gross_profit_usd": 39125000,
            "profit_margin_percentage": 92.06
        }
    """
    gross_profit = revenue_usd - operating_cost_usd
    margin_percentage = (gross_profit / revenue_usd * 100) if revenue_usd > 0 else 0
    
    # Profitability assessment
    if margin_percentage > 70:
        assessment = "Excellent - Highly profitable operation"
    elif margin_percentage > 50:
        assessment = "Good - Healthy profit margin"
    elif margin_percentage > 30:
        assessment = "Moderate - Acceptable profitability"
    else:
        assessment = "Low - Requires cost optimization"
    
    return {
        "revenue_usd": round(revenue_usd, 2),
        "operating_cost_usd": round(operating_cost_usd, 2),
        "gross_profit_usd": round(gross_profit, 2),
        "profit_margin_percentage": round(margin_percentage, 2),
        "profitability_assessment": assessment,
        "breakeven_volume_bopd": round(operating_cost_usd / 85, 0),  # Assuming $85/barrel
        "calculation_timestamp": datetime.now().isoformat()
    }


@tool
def get_market_price_trends(commodity: str = "crude_oil", days_back: int = 30) -> Dict[str, Any]:
    """
    Mengambil trend harga pasar untuk komoditas energi.
    
    Args:
        commodity: Jenis komoditas ("crude_oil", "natural_gas")
        days_back: Jumlah hari historis (default: 30)
    
    Returns:
        Dictionary berisi trend harga dan analisis
    
    Example:
        >>> get_market_price_trends("crude_oil", 30)
        {
            "commodity": "crude_oil",
            "current_price_usd": 85.2,
            "trend": "upward"
        }
    """
    # Mock price data
    base_prices = {
        "crude_oil": 85.0,
        "natural_gas": 3.2  # per MMBTU
    }
    
    current_price = base_prices.get(commodity, 0)
    price_30d_ago = current_price * random.uniform(0.90, 1.05)
    
    trend = "upward" if current_price > price_30d_ago else "downward"
    change_pct = ((current_price - price_30d_ago) / price_30d_ago * 100)
    
    return {
        "commodity": commodity,
        "current_price_usd": round(current_price, 2),
        "price_30_days_ago_usd": round(price_30d_ago, 2),
        "price_change_percentage": round(change_pct, 2),
        "trend": trend,
        "volatility": random.choice(["low", "moderate", "high"]),
        "forecast_outlook": random.choice([
            "Prices expected to stabilize",
            "Potential upward pressure from demand",
            "Risk of correction due to oversupply"
        ]),
        "data_source": "Mock Market Data",
        "last_updated": datetime.now().isoformat()
    }


# Export all tools
finance_tools = [
    calculate_revenue_impact,
    analyze_operational_cost,
    calculate_profitability,
    get_market_price_trends
]
