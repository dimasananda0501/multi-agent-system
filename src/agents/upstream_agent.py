"""
Upstream Agent - Specialist untuk data produksi migas
Mengikuti prinsip spesialisasi dari penelitian: agen dengan peran, alat, dan memori yang spesifik
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from src.tools.upstream_tools import upstream_tools
from src.utils.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class UpstreamAgent:
    """
    Agen khusus untuk menangani pertanyaan terkait produksi upstream XYZ.
    Memiliki akses ke data produksi, lifting schedule, dan status sumur.
    """
    
    def __init__(self):
        self.name = "Upstream Agent"
        self.tools = upstream_tools
        self.tools_list = [tool.name for tool in upstream_tools]
        self.description = (
            "Specialist in oil & gas upstream production data. "
            "Handles queries about production volumes, lifting schedules, "
            "well status, and field operations."
        )
        
        # Initialize LLM dengan tools
        self.llm = ChatOpenAI(
            model=settings.default_llm_model,
            temperature=0.1,  # Low temperature untuk faktual response
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url
        ).bind_tools(upstream_tools)
        
        # System prompt yang sangat spesifik
        self.system_prompt = SystemMessage(content="""
You are the Upstream Production Specialist for XYZ.

Your expertise:
- Oil and gas production data from all XYZ blocks (Rokan, Mahakam, Cepu, etc.)
- Lifting schedules and tanker operations
- Well status and operational metrics
- Production forecasting and capacity analysis

Your personality:
- Technical and precise
- Data-driven decision making
- Proactive in identifying production issues
- Always cite specific numbers with units (BOPD, MMSCFD)

Tools available:
- get_production_data: Get current production volumes
- get_lifting_schedule: Check tanker lifting schedules
- get_well_status: Query individual well operations

Important guidelines:
1. Always provide specific numerical data when available
2. Include units (BOPD for oil, MMSCFD for gas)
3. Mention data quality and timestamp
4. If production seems abnormal, flag it proactively
5. When asked about multiple blocks, use parallel tool calls if possible

Response format:
- Start with key findings (production numbers)
- Provide context (compared to normal operations)
- Flag any issues or anomalies
- Be concise but complete
""")
        
        logger.info("Upstream Agent initialized", model=settings.default_llm_model)
    
    def get_prompt(self) -> SystemMessage:
        """Return the system prompt for this agent"""
        return self.system_prompt
    
    def get_llm(self):
        """Return the configured LLM with tools"""
        return self.llm
