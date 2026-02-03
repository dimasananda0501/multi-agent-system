# Architecture Documentation - XYZ AI Nexus

## System Overview

XYZ AI Nexus adalah sistem multi-agent yang mengimplementasikan **Hub-and-Spoke Architecture** (Orchestrator-Workers Pattern) untuk menangani query kompleks yang melibatkan berbagai domain operasional XYZ.

## Design Principles

### 1. Desentralisasi Kognitif
Beban kognitif didistribusikan ke agen-agen spesialis, bukan dibebankan pada satu model monolitik. Ini memungkinkan:
- Konteks yang lebih fokus per agen
- Reduced hallucination rate
- Better error isolation
- Easier debugging

### 2. Spesialisasi Agen
Setiap agen memiliki:
- **Domain expertise** yang spesifik
- **Tools** yang relevan dengan domain
- **System prompt** yang detail dan persona-driven
- **Temperature** yang low (0.1) untuk faktual responses

### 3. Isolasi Konteks
Agen tidak perlu mengetahui detail internal agen lain. Orchestrator mengelola information flow:
- Mengurangi noise dalam context window
- Mencegah confusion antar domain
- Meningkatkan akurasi responses

## Component Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                         USER LAYER                            │
│  (Web UI / Mobile App / API Clients / Internal Systems)      │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            │ HTTP/REST
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │           FastAPI Application                       │     │
│  │  - Authentication & Authorization                   │     │
│  │  - Rate Limiting                                    │     │
│  │  - Request Validation (Pydantic)                    │     │
│  │  - Error Handling                                   │     │
│  │  - Logging & Monitoring                             │     │
│  └────────────────────────────────────────────────────┘     │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                         │
│  ┌────────────────────────────────────────────────────┐     │
│  │         ORCHESTRATOR AGENT                          │     │
│  │  - Intent Classification (LLM-based)                │     │
│  │  - Dynamic Routing                                  │     │
│  │  - State Management (LangGraph)                     │     │
│  │  - Multi-Agent Coordination                         │     │
│  │  - Response Synthesis                               │     │
│  └────────────────────────────────────────────────────┘     │
└───────────────────────┬──────────────┬───────────────────────┘
                        │              │
        ┌───────────────┴──────┬───────┴──────────┐
        │                      │                   │
        ▼                      ▼                   ▼
┌──────────────┐     ┌──────────────┐    ┌──────────────┐
│   UPSTREAM   │     │  LOGISTICS   │    │   FINANCE    │
│    AGENT     │     │    AGENT     │    │    AGENT     │
│              │     │              │    │              │
│ - Production │     │ - Vessel     │    │ - Revenue    │
│   Data       │     │   Tracking   │    │   Calc       │
│ - Well       │     │ - Weather    │    │ - Cost       │
│   Status     │     │   Forecast   │    │   Analysis   │
│ - Lifting    │     │ - Delivery   │    │ - Profit     │
│   Schedule   │     │   Status     │    │   Margins    │
└──────┬───────┘     └──────┬───────┘    └──────┬───────┘
       │                    │                    │
       │                    │                    │
       ▼                    ▼                    ▼
┌──────────────────────────────────────────────────────────────┐
│                        TOOL LAYER                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │  Upstream  │  │ Logistics  │  │  Finance   │             │
│  │   Tools    │  │   Tools    │  │   Tools    │             │
│  │            │  │            │  │            │             │
│  │ - get_prod │  │ - track    │  │ - calc_rev │             │
│  │ - get_lift │  │ - weather  │  │ - analyze  │             │
│  │ - well_sta │  │ - delivery │  │ - profit   │             │
│  └────────────┘  └────────────┘  └────────────┘             │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                     DATA & SERVICES LAYER                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │   Redis    │  │  Chroma DB │  │  External  │             │
│  │  (Cache &  │  │  (Vector   │  │    APIs    │             │
│  │   State)   │  │  Memory)   │  │  (SAP/PI)  │             │
│  └────────────┘  └────────────┘  └────────────┘             │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

### Example: Simple Query (Single Agent)

**Query**: "What is the current production in Rokan block?"

```
1. User → API Gateway
   POST /query {"query": "What is the current production in Rokan block?"}

2. API Gateway → Orchestrator
   Initialize AgentState with user query

3. Orchestrator: Intent Classification
   LLM analyzes query → Determines: "UPSTREAM"
   
4. Orchestrator → Upstream Agent
   Routes query to Upstream Agent with relevant context

5. Upstream Agent: Processing
   - Reads system prompt (expertise in production data)
   - Analyzes query: needs production data
   - Decides to call tool: get_production_data("Rokan")

6. Upstream Agent → Tool Execution
   Tool returns: {
     "block": "Rokan",
     "oil_production_bopd": 150000,
     "gas_production_mmscfd": 450,
     "status": "operational"
   }

7. Upstream Agent: Response Generation
   LLM synthesizes tool result into natural language:
   "The Rokan block is currently producing 150,000 BOPD..."

8. Upstream Agent → Orchestrator
   Returns response with metadata

9. Orchestrator → API Gateway
   Wraps response with routing info, execution time, etc.

10. API Gateway → User
    JSON response with final answer
```

### Example: Complex Query (Multi-Agent)

**Query**: "What's the profitability of Rokan considering current production and shipping delays?"

```
1-3. [Same as above: User → API → Orchestrator → Classification]

4. Orchestrator Classification
   LLM determines: "ALL_AGENTS" (Upstream + Logistics + Finance)

5. Orchestrator: Parallel Execution Plan
   - Agent 1: Upstream → Get Rokan production
   - Agent 2: Logistics → Check shipping delays
   - Agent 3: Finance → Calculate profitability

6. Parallel Agent Execution
   
   6a. Upstream Agent:
       Tool: get_production_data("Rokan")
       Result: 150,000 BOPD
   
   6b. Logistics Agent:
       Tool: get_delivery_status("Rokan")
       Result: 4-6 hour delay due to weather
   
   6c. Finance Agent:
       Tool: calculate_profitability(...)
       Result: Margin 92%, assessment "Excellent"

7. Orchestrator: Synthesis
   Combines insights from all 3 agents:
   - Production volume
   - Shipping delay impact
   - Financial implications
   
   Creates unified response highlighting connections

8. Orchestrator → API Gateway → User
   Integrated response with multi-dimensional insights
```

## State Management

### AgentState Schema

```python
class AgentState(TypedDict):
    # Message history (append-only)
    messages: List[BaseMessage]
    
    # User context
    user_id: str
    session_id: str
    user_role: str  # For RBAC
    
    # Routing
    next_agent: Optional[str]
    current_agent: Optional[str]
    intent_classification: str
    
    # Task tracking
    task_completed: bool
    iterations: int
    max_iterations: int
    
    # Results
    intermediate_data: Dict[str, Any]
    final_response: Optional[str]
```

State flows through the system:
1. Initialized with user query
2. Updated by each agent
3. Passed between agents via Orchestrator
4. Final state contains complete conversation history

## Agent Design

### Agent Structure

```python
class SpecialistAgent:
    def __init__(self):
        self.name = "Agent Name"
        self.description = "What this agent does"
        
        # LLM with bound tools
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1  # Low for factual
        ).bind_tools(agent_tools)
        
        # Detailed system prompt
        self.system_prompt = SystemMessage(content="""
        You are a specialist in [domain].
        
        Your expertise:
        - [Skill 1]
        - [Skill 2]
        
        Your personality:
        - [Trait 1]
        - [Trait 2]
        
        Tools available:
        - [Tool 1]: [Description]
        - [Tool 2]: [Description]
        
        Guidelines:
        1. [Guideline 1]
        2. [Guideline 2]
        
        Response format:
        - [Format instruction]
        """)
```

### Tool Design (MCP-Compatible)

```python
@tool
def tool_name(param: type) -> Dict[str, Any]:
    """
    Detailed description of what tool does.
    
    Args:
        param: Description with type and examples
    
    Returns:
        Dictionary with specific structure documented
    
    Example:
        >>> tool_name("example")
        {"key": "value"}
    """
    # Implementation
    return result
```

## Routing Logic

### Intent Classification

Orchestrator uses LLM for dynamic intent classification:

```
Input: User query
Process: LLM with routing system prompt
Output: One of:
  - UPSTREAM
  - LOGISTICS
  - FINANCE
  - UPSTREAM_LOGISTICS
  - UPSTREAM_FINANCE
  - LOGISTICS_FINANCE
  - ALL_AGENTS
  - CLARIFY
```

**Benefits over Rule-Based:**
- Handles ambiguous queries
- Adapts to natural language
- No need to maintain complex regex patterns
- Learns from context

## Error Handling

### Retry Strategy
- Exponential backoff for API failures
- Max 3 retries per tool call
- Fallback to simpler model if needed

### Graceful Degradation
- If agent fails, return partial results
- Clearly mark which agents succeeded
- Provide actionable error messages

### Circuit Breaker
- If tool consistently fails, mark as unavailable
- Route around failed components
- Alert monitoring systems

## Security

### Authentication
- Optional API key via `X-API-Key` header
- JWT tokens for user sessions
- OAuth2 for enterprise SSO

### Authorization (RBAC)
- User roles: user, manager, admin, cfo
- Tool access restricted by role
- Sensitive data filtered based on permissions

### Data Privacy
- No storage of conversation content (unless opted in)
- API keys encrypted at rest
- Audit logs for sensitive operations

## Observability

### Logging
- Structured logs (JSON) with contextual data
- Request ID for tracing
- Agent execution traces

### Metrics
- Request latency (p50, p95, p99)
- Token usage per agent
- Cache hit rates
- Error rates by agent

### Tracing
- LangSmith for LLM call tracing
- Full conversation flow visualization
- Tool call inspection

## Scaling Strategy

### Horizontal Scaling
- Stateless API servers
- Shared Redis for caching
- Load balancer for distribution

### Vertical Scaling
- Increase memory for larger context windows
- GPU acceleration for self-hosted models

### Cost Optimization
- Cache frequent queries
- Route to cheaper models when possible
- Batch tool calls
- Token limit enforcement

## Future Enhancements

### Planned Features
1. **Memory Persistence**: Long-term memory across sessions
2. **Human-in-the-Loop**: Approval workflows for sensitive operations
3. **Graph RAG**: Knowledge graph for complex relationships
4. **Multi-Modal**: Support for images, PDFs, Excel files
5. **Streaming**: Real-time response streaming
6. **Agent Marketplace**: Pluggable third-party agents

### Research Areas
- Self-improving agents via RL
- Automatic prompt optimization
- Cost-aware routing
- Adversarial testing for robustness

---

**Architecture Version**: 1.0  
**Last Updated**: February 2026  
**Maintainer**: XYZ Digital Team
