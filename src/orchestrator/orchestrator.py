"""
Orchestrator Agent - The Brain of Multi-Agent System
Mengikuti pola Hub-and-Spoke dari penelitian: 
- Kontrol terpusat untuk pelacakan status
- Fleksibilitas dinamis dalam routing
- Isolasi konteks per agen
"""
from typing import Literal, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from src.utils.state import AgentState
from src.utils.config import settings
from src.utils.logger import get_logger
from src.agents.upstream_agent import UpstreamAgent
from src.agents.logistics_agent import LogisticsAgent
from src.agents.finance_agent import FinanceAgent

logger = get_logger(__name__)


class OrchestratorAgent:
    """
    Orchestrator yang bertindak sebagai 'project manager' dalam sistem multi-agent.
    Tidak memiliki tools sendiri - hanya menganalisis intent dan routing.
    """
    
    def __init__(self):
        self.name = "Orchestrator"
        
        # Initialize specialist agents
        self.upstream_agent = UpstreamAgent()
        self.logistics_agent = LogisticsAgent()
        self.finance_agent = FinanceAgent()
        
        # Router LLM - menggunakan model yang lebih kuat untuk reasoning
        self.router_llm = ChatOpenAI(
            model=settings.orchestrator_model,
            temperature=0,  # Deterministic routing
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url
        )
        
        # System prompt untuk routing
        self.system_prompt = SystemMessage(content="""
You are the Orchestrator for XYZ AI Nexus - a multi-agent system.

Your role is to:
1. Understand the user's intent and question
2. Determine which specialist agent(s) should handle it
3. Route the query to the appropriate agent(s)
4. Synthesize responses when multiple agents are involved

Available Specialist Agents:
- UPSTREAM: Production data, lifting schedules, well status, field operations
- LOGISTICS: Vessel tracking, weather, shipping delays, delivery status  
- FINANCE: Revenue calculations, cost analysis, profitability, market trends

Routing Rules:
- If query is about PRODUCTION/VOLUMES/WELLS → route to UPSTREAM
- If query is about SHIPPING/VESSELS/WEATHER/DELIVERY → route to LOGISTICS
- If query is about REVENUE/COSTS/PROFITS/PRICES → route to FINANCE
- If query involves MULTIPLE domains → identify ALL relevant agents
- If query is ambiguous → ask clarifying question

Examples:
"What's the production in Rokan?" → UPSTREAM
"Where is MT XYZ Prime?" → LOGISTICS
"How much revenue from 500k barrels?" → FINANCE
"Status of Rokan production and its shipment to Balongan?" → UPSTREAM + LOGISTICS
"Profitability of Rokan block considering shipping delays?" → ALL THREE

Your response must be ONE of:
- "UPSTREAM" (only upstream needed)
- "LOGISTICS" (only logistics needed)
- "FINANCE" (only finance needed)
- "UPSTREAM_LOGISTICS" (both needed)
- "UPSTREAM_FINANCE" (both needed)
- "LOGISTICS_FINANCE" (both needed)
- "ALL_AGENTS" (all three needed)
- "CLARIFY" (need more info from user)

Respond with ONLY the routing decision, nothing else.
""")
        
        logger.info("Orchestrator initialized", 
                   router_model=settings.orchestrator_model,
                   specialist_agents=["upstream", "logistics", "finance"])
    
    def classify_intent(self, query: str) -> str:
        """
        Classify user intent and determine routing.
        This is the 'brain' function that decides which agent(s) to call.
        """
        messages = [
            self.system_prompt,
            HumanMessage(content=f"User query: {query}")
        ]
        
        response = self.router_llm.invoke(messages)
        routing_decision = response.content.strip().upper()
        
        logger.info("Intent classified", 
                   query=query[:100], 
                   routing=routing_decision)
        
        return routing_decision
    
    def build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow.
        This implements the Hub-and-Spoke architecture.
        """
        # Initialize graph
        workflow = StateGraph(AgentState)
        
        # Add nodes for each specialist agent
        workflow.add_node("upstream", self._upstream_node)
        workflow.add_node("logistics", self._logistics_node)
        workflow.add_node("finance", self._finance_node)
        workflow.add_node("synthesizer", self._synthesizer_node)
        
        # Add tool execution nodes
        workflow.add_node("upstream_tools", 
                         ToolNode(self.upstream_agent.tools))
        workflow.add_node("logistics_tools", 
                         ToolNode(self.logistics_agent.tools))
        workflow.add_node("finance_tools", 
                         ToolNode(self.finance_agent.tools))
        
        # Add router node
        workflow.add_node("router", self._router_node)
        workflow.set_entry_point("router")
        
        # Define routing logic
        workflow.add_conditional_edges(
            "router",
            self._route_to_agent,
            {
                "upstream": "upstream",
                "logistics": "logistics",
                "finance": "finance",
                "clarify": END
            }
        )
        
        workflow.add_conditional_edges(
            "upstream",
            self._should_continue,
            {
                "continue": "upstream_tools",
                "synthesizer": "synthesizer",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "logistics",
            self._should_continue,
            {
                "continue": "logistics_tools",
                "synthesizer": "synthesizer",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "finance",
            self._should_continue,
            {
                "continue": "finance_tools",
                "synthesizer": "synthesizer",
                "end": END
            }
        )
        
        # Tool nodes return to their respective agents
        workflow.add_edge("upstream_tools", "upstream")
        workflow.add_edge("logistics_tools", "logistics")
        workflow.add_edge("finance_tools", "finance")
        
        # Synthesizer ends the workflow
        workflow.add_edge("synthesizer", END)
        
        return workflow

    def _router_node(self, state: AgentState) -> AgentState:
        """Node to classify intent if not already done"""
        if not state.get("intent_classification"):
            query = state["messages"][-1].content
            routing = self.classify_intent(query)
            return {"intent_classification": routing}
        return state

    def _route_to_agent(self, state: AgentState) -> str:
        """Route to the first agent based on classification"""
        routing = state.get("intent_classification", "")
        
        if "UPSTREAM" in routing:
            return "upstream"
        elif "LOGISTICS" in routing:
            return "logistics"
        elif "FINANCE" in routing:
            return "finance"
        else:
            return "clarify"

    async def run(self, query: str, user_id: str = "anonymous", user_role: str = "user") -> Dict[str, Any]:
        """
        Run the full multi-agent workflow for a query.
        """
        app = self.build_graph().compile()
        
        initial_state: AgentState = {
            "messages": [HumanMessage(content=query)],
            "user_id": user_id,
            "session_id": "",
            "user_role": user_role,
            "next_agent": None,
            "current_agent": None,
            "intent_classification": None,
            "task_completed": False,
            "iterations": 0,
            "max_iterations": settings.max_iterations,
            "intermediate_data": {},
            "final_response": None,
            "response_metadata": {}
        }
        
        config = {"configurable": {"thread_id": user_id}}
        
        # Run the graph
        final_state = await app.ainvoke(initial_state, config)
        
        return {
            "response": final_state.get("final_response") or final_state["messages"][-1].content,
            "agents_involved": self._get_agents_involved(final_state),
            "routing_decision": final_state.get("intent_classification", "UNKNOWN")
        }

    def _get_agents_involved(self, state: AgentState) -> list[str]:
        """Extract involved agents from state"""
        agents = []
        routing = state.get("intent_classification", "")
        if "UPSTREAM" in routing: agents.append("upstream")
        if "LOGISTICS" in routing: agents.append("logistics")
        if "FINANCE" in routing: agents.append("finance")
        return agents

    def _upstream_node(self, state: AgentState) -> AgentState:
        """Execute upstream agent"""
        logger.info("Executing upstream agent")
        
        messages = [self.upstream_agent.get_prompt()] + state["messages"]
        response = self.upstream_agent.get_llm().invoke(messages)
        
        return {
            "messages": [response],
            "current_agent": "upstream"
        }
    
    def _logistics_node(self, state: AgentState) -> AgentState:
        """Execute logistics agent"""
        logger.info("Executing logistics agent")
        
        messages = [self.logistics_agent.get_prompt()] + state["messages"]
        response = self.logistics_agent.get_llm().invoke(messages)
        
        return {
            "messages": [response],
            "current_agent": "logistics"
        }
    
    def _finance_node(self, state: AgentState) -> AgentState:
        """Execute finance agent"""
        logger.info("Executing finance agent")
        
        messages = [self.finance_agent.get_prompt()] + state["messages"]
        response = self.finance_agent.get_llm().invoke(messages)
        
        return {
            "messages": [response],
            "current_agent": "finance"
        }
    
    def _synthesizer_node(self, state: AgentState) -> AgentState:
        """
        Synthesize responses from multiple agents into final answer.
        """
        logger.info("Synthesizing multi-agent responses")
        
        agent_responses = []
        for msg in state["messages"]:
            if hasattr(msg, 'content') and msg.content and not isinstance(msg, HumanMessage):
                agent_responses.append(msg.content)
        
        synthesis_prompt = f"""
        You are synthesizing responses from multiple XYZ specialist agents.
        
        Agent Responses:
        {chr(10).join(f"- {resp}" for resp in agent_responses[-3:])}
        
        Create a cohesive, integrated final response.
        """
        
        final_response = self.router_llm.invoke([HumanMessage(content=synthesis_prompt)])
        
        return {
            "messages": [final_response],
            "final_response": final_response.content,
            "task_completed": True
        }
    
    def _should_continue(
        self, 
        state: AgentState
    ) -> Literal["continue", "synthesizer", "end"]:
        """
        Determine if agent should continue.
        """
        last_message = state["messages"][-1]
        
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "continue"
        
        if state.get("task_completed", False):
            return "end"
        
        return "end"
