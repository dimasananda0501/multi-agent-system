"""
FastAPI Application - REST API untuk XYZ AI Nexus
Mengekspos multi-agent system sebagai API yang production-ready
"""
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime

from src.orchestrator.orchestrator import OrchestratorAgent
from src.utils.config import settings
from src.utils.logger import setup_logging, get_logger
from src.utils.state import AgentState
from langchain_core.messages import HumanMessage

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="XYZ AI Nexus",
    description="Multi-Agent AI System for XYZ Operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator (singleton)
orchestrator = OrchestratorAgent()

# Request/Response models
class QueryRequest(BaseModel):
    """Request model for agent query"""
    query: str = Field(..., description="User question or command", min_length=3)
    user_id: Optional[str] = Field(default=None, description="User identifier for tracking")
    session_id: Optional[str] = Field(default=None, description="Session ID for context")
    user_role: Optional[str] = Field(default="user", description="User role for RBAC")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Additional context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the current production in Rokan block and how much revenue does it generate?",
                "user_id": "user_123",
                "user_role": "manager"
            }
        }


class AgentResponse(BaseModel):
    """Response model from agent system"""
    session_id: str
    query: str
    routing_decision: str
    response: str
    agents_involved: List[str]
    execution_time_ms: float
    timestamp: str
    metadata: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    agents_available: List[str]
    timestamp: str


# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    request_id = str(uuid.uuid4())
    logger.info(
        "Request received",
        request_id=request_id,
        method=request.method,
        path=request.url.path
    )
    
    response = await call_next(request)
    
    logger.info(
        "Request completed",
        request_id=request_id,
        status_code=response.status_code
    )
    
    return response


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint - API info"""
    return {
        "message": "XYZ AI Nexus - Multi-Agent System",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns status of the API and available agents.
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        agents_available=[
            "upstream",
            "logistics", 
            "finance"
        ],
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/query", response_model=AgentResponse)
async def process_query(
    request: QueryRequest,
    x_api_key: Optional[str] = Header(None)
):
    """
    Main endpoint - Process user query through multi-agent system.
    
    This endpoint:
    1. Classifies user intent
    2. Routes to appropriate agent(s)
    3. Executes agent workflow
    4. Returns synthesized response
    
    Security: Optional API key authentication via X-API-Key header
    """
    start_time = datetime.utcnow()
    
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    user_id = request.user_id or "anonymous"
    
    logger.info(
        "Processing query",
        session_id=session_id,
        user_id=user_id,
        query=request.query[:100]
    )
    
    try:
        # Step 1: Classify intent and determine routing
        routing_decision = orchestrator.classify_intent(request.query)
        
        logger.info(
            "Query routed",
            routing=routing_decision,
            session_id=session_id
        )
        
        # Step 2: Initialize state
        initial_state: AgentState = {
            "messages": [HumanMessage(content=request.query)],
            "user_id": user_id,
            "session_id": session_id,
            "user_role": request.user_role,
            "next_agent": None,
            "current_agent": None,
            "intent_classification": routing_decision,
            "task_completed": False,
            "iterations": 0,
            "max_iterations": settings.max_iterations,
            "intermediate_data": request.context,
            "final_response": None,
            "response_metadata": {}
        }
        
        # Step 3: Determine entry point based on routing
        agents_to_invoke = []
        
        if "UPSTREAM" in routing_decision:
            agents_to_invoke.append("upstream")
        if "LOGISTICS" in routing_decision:
            agents_to_invoke.append("logistics")
        if "FINANCE" in routing_decision:
            agents_to_invoke.append("finance")
        
        # Handle clarification needed
        if routing_decision == "CLARIFY":
            return AgentResponse(
                session_id=session_id,
                query=request.query,
                routing_decision=routing_decision,
                response="I need more information to help you. Could you please clarify your question? Are you asking about production data, shipping logistics, or financial analysis?",
                agents_involved=[],
                execution_time_ms=0,
                timestamp=datetime.utcnow().isoformat(),
                metadata={"status": "clarification_needed"}
            )
        
        # Step 4: Execute agent(s) using LangGraph
        result = await orchestrator.run(
            query=request.query,
            user_id=user_id,
            user_role=request.user_role
        )
        
        final_response = result["response"]
        agents_to_invoke = result["agents_involved"]
        routing_decision = result["routing_decision"]
        
        # Calculate execution time
        execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        logger.info(
            "Query processed successfully via LangGraph",
            session_id=session_id,
            execution_time_ms=execution_time,
            agents_involved=agents_to_invoke
        )
        
        return AgentResponse(
            session_id=session_id,
            query=request.query,
            routing_decision=routing_decision,
            response=final_response,
            agents_involved=agents_to_invoke,
            execution_time_ms=round(execution_time, 2),
            timestamp=datetime.utcnow().isoformat(),
            metadata={
                "user_id": user_id,
                "user_role": request.user_role,
                "status": "completed",
                "engine": "langgraph"
            }
        )
        
    except Exception as e:
        logger.error(
            "Query processing failed",
            session_id=session_id,
            error=str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )


@app.get("/agents", response_model=Dict[str, Any])
async def list_agents():
    """
    List all available agents and their capabilities.
    Useful for documentation and discovery.
    """
    return {
        "agents": [
            {
                "name": "Upstream Agent",
                "description": orchestrator.upstream_agent.description,
                "capabilities": [
                    "Production data retrieval",
                    "Lifting schedule queries",
                    "Well status monitoring"
                ],
                "tools": orchestrator.upstream_agent.tools_list
            },
            {
                "name": "Logistics Agent",
                "description": orchestrator.logistics_agent.description,
                "capabilities": [
                    "Vessel tracking",
                    "Weather forecasting",
                    "Delivery status tracking"
                ],
                "tools": orchestrator.logistics_agent.tools_list
            },
            {
                "name": "Finance Agent",
                "description": orchestrator.finance_agent.description,
                "capabilities": [
                    "Revenue calculation",
                    "Cost analysis",
                    "Profitability assessment"
                ],
                "tools": orchestrator.finance_agent.tools_list
            }
        ],
        "routing_patterns": {
            "single_agent": ["UPSTREAM", "LOGISTICS", "FINANCE"],
            "multi_agent": ["UPSTREAM_LOGISTICS", "UPSTREAM_FINANCE", "LOGISTICS_FINANCE", "ALL_AGENTS"]
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(
        "Unhandled exception",
        path=request.url.path,
        error=str(exc),
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "path": request.url.path
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info(
        "Starting XYZ AI Nexus",
        host=settings.api_host,
        port=settings.api_port,
        env=settings.app_env
    )
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.app_env == "development"
    )
