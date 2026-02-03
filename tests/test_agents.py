"""
Test Suite untuk Multi-Agent System
Mengikuti best practice: testing komprehensif untuk production readiness
"""
import pytest
from unittest.mock import Mock, patch
from src.agents.upstream_agent import UpstreamAgent
from src.agents.logistics_agent import LogisticsAgent
from src.agents.finance_agent import FinanceAgent
from src.orchestrator.orchestrator import OrchestratorAgent
from src.tools.upstream_tools import get_production_data, get_lifting_schedule
from src.tools.logistics_tools import track_vessel, get_weather_forecast
from src.tools.finance_tools import calculate_revenue_impact


class TestUpstreamTools:
    """Test upstream tools functionality"""
    
    def test_get_production_data_rokan(self):
        """Test production data retrieval for Rokan block"""
        result = get_production_data.invoke({"block_name": "Rokan"})
        
        assert result["block"] == "Rokan"
        assert result["oil_production_bopd"] == 150000
        assert result["status"] == "operational"
        assert "date" in result
    
    def test_get_production_data_unknown_block(self):
        """Test production data for unknown block"""
        result = get_production_data.invoke({"block_name": "Unknown"})
        
        assert result["block"] == "Unknown"
        assert result["oil_production_bopd"] == 0
        assert result["status"] == "unknown"
    
    def test_get_lifting_schedule(self):
        """Test lifting schedule retrieval"""
        result = get_lifting_schedule.invoke({
            "block_name": "Mahakam",
            "days_ahead": 7
        })
        
        assert result["block"] == "Mahakam"
        assert "schedule" in result
        assert isinstance(result["schedule"], list)
        assert "total_volume_barrels" in result


class TestLogisticsTools:
    """Test logistics tools functionality"""
    
    def test_track_vessel(self):
        """Test vessel tracking"""
        result = track_vessel.invoke({"vessel_name": "MT XYZ Prime"})
        
        assert result["vessel_name"] == "MT XYZ Prime"
        assert "current_position" in result
        assert "speed_knots" in result
        assert "eta_hours" in result
    
    def test_get_weather_forecast(self):
        """Test weather forecast"""
        result = get_weather_forecast.invoke({
            "location": "Selat Sunda",
            "hours_ahead": 24
        })
        
        assert result["location"] == "Selat Sunda"
        assert "wave_height_meters" in result
        assert "risk_level" in result
        assert result["risk_level"] in ["low", "moderate", "high"]


class TestFinanceTools:
    """Test finance tools functionality"""
    
    def test_calculate_revenue_impact(self):
        """Test revenue calculation"""
        result = calculate_revenue_impact.invoke({
            "oil_volume_barrels": 500000,
            "oil_price_usd": 85.0
        })
        
        assert result["volume_barrels"] == 500000
        assert result["total_revenue_usd"] == 42500000
        assert "total_revenue_idr" in result
    
    def test_calculate_revenue_different_price(self):
        """Test revenue with different oil price"""
        result = calculate_revenue_impact.invoke({
            "oil_volume_barrels": 100000,
            "oil_price_usd": 100.0
        })
        
        assert result["total_revenue_usd"] == 10000000


class TestAgents:
    """Test agent initialization and configuration"""
    
    def test_upstream_agent_init(self):
        """Test upstream agent initialization"""
        agent = UpstreamAgent()
        
        assert agent.name == "Upstream Agent"
        assert agent.llm is not None
        assert len(agent.llm.tools) == 3  # 3 upstream tools
    
    def test_logistics_agent_init(self):
        """Test logistics agent initialization"""
        agent = LogisticsAgent()
        
        assert agent.name == "Logistics Agent"
        assert agent.llm is not None
        assert len(agent.llm.tools) == 3  # 3 logistics tools
    
    def test_finance_agent_init(self):
        """Test finance agent initialization"""
        agent = FinanceAgent()
        
        assert agent.name == "Finance Agent"
        assert agent.llm is not None
        assert len(agent.llm.tools) == 4  # 4 finance tools


class TestOrchestrator:
    """Test orchestrator routing logic"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance for tests"""
        return OrchestratorAgent()
    
    def test_orchestrator_init(self, orchestrator):
        """Test orchestrator initialization"""
        assert orchestrator.name == "Orchestrator"
        assert orchestrator.upstream_agent is not None
        assert orchestrator.logistics_agent is not None
        assert orchestrator.finance_agent is not None
    
    @pytest.mark.skip(reason="Requires DeepSeek API key")
    def test_classify_upstream_intent(self, orchestrator):
        """Test intent classification for upstream query"""
        query = "What is the production in Rokan block?"
        routing = orchestrator.classify_intent(query)
        
        assert "UPSTREAM" in routing
    
    @pytest.mark.skip(reason="Requires DeepSeek API key")
    def test_classify_logistics_intent(self, orchestrator):
        """Test intent classification for logistics query"""
        query = "Where is MT XYZ Prime right now?"
        routing = orchestrator.classify_intent(query)
        
        assert "LOGISTICS" in routing
    
    @pytest.mark.skip(reason="Requires DeepSeek API key")
    def test_classify_multi_agent_intent(self, orchestrator):
        """Test intent classification for multi-agent query"""
        query = "What is the production in Rokan and when will it be shipped?"
        routing = orchestrator.classify_intent(query)
        
        assert "UPSTREAM" in routing or "ALL" in routing


class TestAPI:
    """Test FastAPI endpoints (requires running server)"""
    
    @pytest.mark.skip(reason="Integration test - requires running API")
    def test_health_endpoint(self):
        """Test health check endpoint"""
        from fastapi.testclient import TestClient
        from main import app
        
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "agents_available" in data
    
    @pytest.mark.skip(reason="Integration test - requires running API and DeepSeek key")
    def test_query_endpoint(self):
        """Test query processing endpoint"""
        from fastapi.testclient import TestClient
        from main import app
        
        client = TestClient(app)
        response = client.post(
            "/query",
            json={
                "query": "What is the production in Rokan?",
                "user_id": "test_user"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "routing_decision" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
