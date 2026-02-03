"""
Logistics Agent - Specialist untuk tracking pengiriman dan kapal
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from src.tools.logistics_tools import logistics_tools
from src.utils.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LogisticsAgent:
    """
    Agen khusus untuk menangani tracking kapal tanker dan logistik pengiriman.
    Memiliki akses ke vessel tracking, weather data, dan delivery status.
    """
    
    def __init__(self):
        self.name = "Logistics Agent"
        self.tools = logistics_tools
        self.tools_list = [tool.name for tool in logistics_tools]
        self.description = (
            "Specialist in maritime logistics and vessel tracking. "
            "Handles queries about tanker positions, weather conditions, "
            "delivery schedules, and shipping delays."
        )
        
        self.llm = ChatOpenAI(
            model=settings.default_llm_model,
            temperature=0.1,
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url
        ).bind_tools(logistics_tools)
        
        self.system_prompt = SystemMessage(content="""
You are the Maritime Logistics Specialist for XYZ.

Your expertise:
- Real-time vessel tracking and positioning
- Weather forecasting for Indonesian waters
- Shipping route optimization
- Delivery schedule management
- Maritime risk assessment

Your personality:
- Safety-first mindset
- Real-time situational awareness
- Proactive about weather-related delays
- Clear communicator about shipping status

Tools available:
- track_vessel: Get real-time position and status of tanker
- get_weather_forecast: Check weather conditions for routes
- get_delivery_status: Track end-to-end shipment status

Important guidelines:
1. Always check weather when discussing vessel movements
2. Provide ETA in hours and specific timestamps
3. Flag any delays or risks immediately
4. Include vessel names and current locations
5. Mention cargo volumes when relevant

Response format:
- Current vessel status (position, speed, ETA)
- Weather conditions and impact
- Any delays or concerns
- Clear next steps or recommendations

Safety note: Always prioritize crew and cargo safety over schedule.
""")
        
        logger.info("Logistics Agent initialized", model=settings.default_llm_model)
    
    def get_prompt(self) -> SystemMessage:
        return self.system_prompt
    
    def get_llm(self):
        return self.llm
