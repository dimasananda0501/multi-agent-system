"""
State Schema untuk Multi-Agent System
Mengikuti best practice dari penelitian: konteks terfragmentasi dan terisolasi per agen
"""
from typing import TypedDict, Annotated, List, Optional, Dict, Any
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """
    Schema state global yang dibawa antar agen.
    Menggunakan operator.add untuk append-only message history.
    """
    # Message history (append-only)
    messages: Annotated[List[BaseMessage], operator.add]
    
    # User context
    user_id: str
    session_id: str
    user_role: Optional[str]  # Untuk RBAC
    
    # Routing & orchestration
    next_agent: Optional[str]
    current_agent: Optional[str]
    intent_classification: Optional[str]
    
    # Task tracking
    task_completed: bool
    iterations: int
    max_iterations: int
    
    # Intermediate results
    intermediate_data: Dict[str, Any]
    
    # Final output
    final_response: Optional[str]
    response_metadata: Dict[str, Any]


class UpstreamAgentState(TypedDict):
    """State khusus untuk Upstream Agent - data produksi migas"""
    production_data: Optional[Dict[str, Any]]
    well_status: Optional[List[Dict[str, Any]]]
    lifting_schedule: Optional[Dict[str, Any]]


class LogisticsAgentState(TypedDict):
    """State khusus untuk Logistics Agent - tracking kapal & pengiriman"""
    vessel_tracking: Optional[List[Dict[str, Any]]]
    weather_data: Optional[Dict[str, Any]]
    delivery_status: Optional[Dict[str, Any]]


class FinanceAgentState(TypedDict):
    """State khusus untuk Finance Agent - analisis revenue & cost"""
    revenue_data: Optional[Dict[str, Any]]
    cost_analysis: Optional[Dict[str, Any]]
    profitability_metrics: Optional[Dict[str, Any]]
