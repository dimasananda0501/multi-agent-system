# API Reference - XYZ AI Nexus

Complete API documentation untuk XYZ AI Nexus Multi-Agent System.

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
HF Spaces: https://YOUR_USERNAME-xyz-ai-nexus.hf.space
```

## Authentication

Optional API key authentication via header:

```http
X-API-Key: your_api_key_here
```

## Endpoints

### `GET /`

Root endpoint - API information.

**Response:**
```json
{
  "message": "XYZ AI Nexus - Multi-Agent System",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "agents_available": ["upstream", "logistics", "finance"],
  "timestamp": "2026-02-02T10:30:00Z"
}
```

**Status Codes:**
- `200`: Service healthy
- `503`: Service unavailable

---

### `POST /query`

Main endpoint - Process user query through multi-agent system.

**Request Body:**

```json
{
  "query": "string (required, min 3 chars)",
  "user_id": "string (optional)",
  "session_id": "string (optional)",
  "user_role": "string (optional, default: user)",
  "context": "object (optional)"
}
```

**Example Request:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_key" \
  -d '{
    "query": "What is the current production in Rokan block?",
    "user_id": "manager_001",
    "user_role": "manager"
  }'
```

**Response:**

```json
{
  "session_id": "uuid-string",
  "query": "What is the current production in Rokan block?",
  "routing_decision": "UPSTREAM",
  "response": "The Rokan block is currently producing 150,000 BOPD (Barrels of Oil Per Day) and 450 MMSCFD (Million Standard Cubic Feet per Day) of gas. The block is operational with 2,500 active wells. Data quality: real-time, as of 2026-02-02.",
  "agents_involved": ["upstream"],
  "execution_time_ms": 1234.56,
  "timestamp": "2026-02-02T10:30:00Z",
  "metadata": {
    "user_id": "manager_001",
    "user_role": "manager",
    "status": "completed"
  }
}
```

**Routing Decisions:**

| Decision | Description | Agents Involved |
|----------|-------------|-----------------|
| `UPSTREAM` | Production data queries | Upstream Agent |
| `LOGISTICS` | Shipping/vessel queries | Logistics Agent |
| `FINANCE` | Financial analysis queries | Finance Agent |
| `UPSTREAM_LOGISTICS` | Production + shipping | Upstream + Logistics |
| `UPSTREAM_FINANCE` | Production + revenue | Upstream + Finance |
| `LOGISTICS_FINANCE` | Shipping + costs | Logistics + Finance |
| `ALL_AGENTS` | Complex multi-domain | All three agents |
| `CLARIFY` | Ambiguous query | None (needs clarification) |

**Status Codes:**
- `200`: Success
- `400`: Invalid request (bad query format)
- `401`: Unauthorized (invalid API key)
- `500`: Server error

**Error Response:**
```json
{
  "error": "Internal server error",
  "message": "Detailed error message",
  "path": "/query"
}
```

---

### `GET /agents`

List all available agents and their capabilities.

**Response:**

```json
{
  "agents": [
    {
      "name": "Upstream Agent",
      "description": "Specialist in oil & gas upstream production data...",
      "capabilities": [
        "Production data retrieval",
        "Lifting schedule queries",
        "Well status monitoring"
      ],
      "tools": [
        "get_production_data",
        "get_lifting_schedule",
        "get_well_status"
      ]
    },
    {
      "name": "Logistics Agent",
      "description": "Specialist in maritime logistics...",
      "capabilities": [
        "Vessel tracking",
        "Weather forecasting",
        "Delivery status tracking"
      ],
      "tools": [
        "track_vessel",
        "get_weather_forecast",
        "get_delivery_status"
      ]
    },
    {
      "name": "Finance Agent",
      "description": "Specialist in financial analysis...",
      "capabilities": [
        "Revenue calculation",
        "Cost analysis",
        "Profitability assessment"
      ],
      "tools": [
        "calculate_revenue_impact",
        "analyze_operational_cost",
        "calculate_profitability",
        "get_market_price_trends"
      ]
    }
  ],
  "routing_patterns": {
    "single_agent": ["UPSTREAM", "LOGISTICS", "FINANCE"],
    "multi_agent": [
      "UPSTREAM_LOGISTICS",
      "UPSTREAM_FINANCE",
      "LOGISTICS_FINANCE",
      "ALL_AGENTS"
    ]
  }
}
```

---

## Query Examples

### Example 1: Production Data (Upstream)

**Request:**
```json
{
  "query": "What is the oil production in Mahakam block?",
  "user_id": "analyst_001"
}
```

**Response:**
```json
{
  "routing_decision": "UPSTREAM",
  "response": "The Mahakam block is currently producing 85,000 BOPD and 1,200 MMSCFD of gas...",
  "agents_involved": ["upstream"]
}
```

### Example 2: Vessel Tracking (Logistics)

**Request:**
```json
{
  "query": "Where is MT XYZ Prime and when will it arrive?",
  "user_id": "logistics_002"
}
```

**Response:**
```json
{
  "routing_decision": "LOGISTICS",
  "response": "MT XYZ Prime is currently in Selat Sunda, traveling at 12.5 knots. ETA to destination is 18 hours...",
  "agents_involved": ["logistics"]
}
```

### Example 3: Revenue Calculation (Finance)

**Request:**
```json
{
  "query": "Calculate revenue from 500,000 barrels at $85 per barrel",
  "user_id": "finance_003"
}
```

**Response:**
```json
{
  "routing_decision": "FINANCE",
  "response": "Revenue calculation: 500,000 barrels × $85/barrel = $42,500,000 USD (approximately Rp 671,500,000,000 at current exchange rate)...",
  "agents_involved": ["finance"]
}
```

### Example 4: Multi-Agent Query

**Request:**
```json
{
  "query": "What's the status of Rokan production and its shipment to Balongan, considering weather conditions?",
  "user_id": "manager_004"
}
```

**Response:**
```json
{
  "routing_decision": "UPSTREAM_LOGISTICS",
  "response": "Rokan block is producing 150,000 BOPD. The next lifting is scheduled for MT XYZ Prime in 2 days (500,000 barrels to Kilang Balongan). However, weather forecast shows moderate wave heights in Selat Sunda (2.5m), which may cause a 4-6 hour delay...",
  "agents_involved": ["upstream", "logistics"]
}
```

### Example 5: Complex Business Analysis

**Request:**
```json
{
  "query": "Analyze profitability of Cepu block considering current production, operating costs, and shipping delays",
  "user_id": "cfo_005",
  "user_role": "admin"
}
```

**Response:**
```json
{
  "routing_decision": "ALL_AGENTS",
  "response": "Complete profitability analysis: Cepu block produces 35,000 BOPD. Operating cost: $35/barrel. Revenue at $85/barrel: $2.975M daily. However, shipping delays due to weather reduce effective revenue by ~5%. Net profit margin: 58.8% (moderate). Recommendation: Monitor weather patterns and consider route optimization...",
  "agents_involved": ["upstream", "logistics", "finance"]
}
```

---

## Agent Tools Reference

### Upstream Agent Tools

#### `get_production_data(block_name: str)`

Get current production data from oil & gas block.

**Parameters:**
- `block_name`: Name of production block (e.g., "Rokan", "Mahakam", "Cepu")

**Returns:**
```json
{
  "block": "Rokan",
  "date": "2026-02-02",
  "oil_production_bopd": 150000,
  "gas_production_mmscfd": 450,
  "status": "operational",
  "wells_active": 2500,
  "data_quality": "real-time"
}
```

#### `get_lifting_schedule(block_name: str, days_ahead: int)`

Get tanker lifting schedule.

**Parameters:**
- `block_name`: Production block name
- `days_ahead`: Number of days to look ahead (default: 7)

**Returns:**
```json
{
  "block": "Rokan",
  "schedule_period_days": 7,
  "schedule": [
    {
      "date": "2026-02-03",
      "volume_barrels": 500000,
      "vessel": "MT XYZ Prime",
      "destination": "Kilang Balongan"
    }
  ],
  "total_volume_barrels": 1500000
}
```

#### `get_well_status(block_name: str, well_ids: list)`

Get operational status of wells.

**Returns:**
```json
{
  "block": "Rokan",
  "wells": [
    {
      "id": "RKN-001",
      "status": "producing",
      "production_bopd": 125
    },
    {
      "id": "RKN-002",
      "status": "maintenance",
      "downtime_hours": 48
    }
  ]
}
```

### Logistics Agent Tools

#### `track_vessel(vessel_name: str)`

Real-time vessel tracking.

**Returns:**
```json
{
  "vessel_name": "MT XYZ Prime",
  "current_location": "Selat Sunda",
  "current_position": {"latitude": -6.123, "longitude": 106.456},
  "speed_knots": 12.5,
  "status": "on_schedule",
  "eta_hours": 18
}
```

#### `get_weather_forecast(location: str, hours_ahead: int)`

Weather forecast for shipping routes.

**Returns:**
```json
{
  "location": "Selat Sunda",
  "wave_height_meters": 2.5,
  "wind_speed_knots": 18,
  "risk_level": "moderate",
  "navigation_advice": "Proceed with caution. Expect speed reduction."
}
```

#### `get_delivery_status(shipment_id: str)`

End-to-end shipment tracking.

**Returns:**
```json
{
  "shipment_id": "SHP-2026-001",
  "status": "in_transit",
  "progress_percentage": 65,
  "vessel_assigned": "MT XYZ Prime",
  "estimated_arrival": "2026-02-03T14:00:00Z"
}
```

### Finance Agent Tools

#### `calculate_revenue_impact(oil_volume_barrels: int, oil_price_usd: float)`

Calculate revenue from oil volume.

**Returns:**
```json
{
  "volume_barrels": 500000,
  "price_per_barrel_usd": 85.0,
  "total_revenue_usd": 42500000,
  "total_revenue_idr": 671500000000
}
```

#### `analyze_operational_cost(block_name: str, production_volume_bopd: int)`

Analyze operating costs.

**Returns:**
```json
{
  "block": "Rokan",
  "operating_cost_per_barrel_usd": 22.5,
  "total_daily_cost_usd": 3375000,
  "cost_breakdown": {
    "labor_usd": 1181250,
    "maintenance_usd": 843750,
    "energy_usd": 675000
  }
}
```

#### `calculate_profitability(revenue_usd: float, operating_cost_usd: float)`

Calculate profit margins.

**Returns:**
```json
{
  "revenue_usd": 42500000,
  "operating_cost_usd": 3375000,
  "gross_profit_usd": 39125000,
  "profit_margin_percentage": 92.06,
  "profitability_assessment": "Excellent"
}
```

---

## Rate Limits

| Tier | Requests/Hour | Requests/Day |
|------|---------------|--------------|
| Free | 100 | 1,000 |
| Pro | 1,000 | 10,000 |
| Enterprise | Custom | Custom |

**Rate limit headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1675329600
```

---

## Errors

### Error Response Format

```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "path": "/query",
  "timestamp": "2026-02-02T10:30:00Z"
}
```

### Common Errors

| Code | Error | Description |
|------|-------|-------------|
| 400 | Bad Request | Invalid query format or parameters |
| 401 | Unauthorized | Missing or invalid API key |
| 429 | Rate Limit | Too many requests |
| 500 | Server Error | Internal processing error |
| 503 | Service Unavailable | Agent temporarily unavailable |

---

## SDKs & Libraries

### Python

```python
import requests

class XYZAIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["X-API-Key"] = api_key
    
    def query(self, query, user_id="anonymous"):
        response = requests.post(
            f"{self.base_url}/query",
            json={"query": query, "user_id": user_id},
            headers=self.headers
        )
        return response.json()

# Usage
client = XYZAIClient("http://localhost:8000")
result = client.query("What is production in Rokan?")
print(result["response"])
```

### JavaScript/TypeScript

```javascript
class XYZAIClient {
  constructor(baseUrl, apiKey = null) {
    this.baseUrl = baseUrl;
    this.headers = {
      'Content-Type': 'application/json',
      ...(apiKey && { 'X-API-Key': apiKey })
    };
  }
  
  async query(query, userId = 'anonymous') {
    const response = await fetch(`${this.baseUrl}/query`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({ query, user_id: userId })
    });
    return response.json();
  }
}

// Usage
const client = new XYZAIClient('http://localhost:8000');
const result = await client.query('What is production in Rokan?');
console.log(result.response);
```

---

## Interactive Documentation

Visit `/docs` for interactive Swagger UI documentation where you can:
- Test endpoints directly
- See request/response schemas
- Download OpenAPI specification

---

**API Version**: 1.0.0  
**Last Updated**: February 2026  
**Support**: support@xyz-nexus.ai
