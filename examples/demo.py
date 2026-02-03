"""
Example Usage Script - XYZ AI Nexus
Demonstrasi berbagai skenario penggunaan multi-agent system
"""
import asyncio
import requests
import json
from typing import Dict, Any


class XYZAIClient:
    """
    Simple client untuk berinteraksi dengan XYZ AI Nexus API
    """
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["X-API-Key"] = api_key
    
    def query(self, query: str, user_id: str = "demo_user", user_role: str = "manager") -> Dict[str, Any]:
        """
        Send query to AI Nexus and get response
        """
        url = f"{self.base_url}/query"
        payload = {
            "query": query,
            "user_id": user_id,
            "user_role": user_role
        }
        
        print(f"\n{'='*80}")
        print(f"🔍 Query: {query}")
        print(f"{'='*80}")
        
        response = requests.post(url, json=payload, headers=self.headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n📊 Routing Decision: {result['routing_decision']}")
            print(f"🤖 Agents Involved: {', '.join(result['agents_involved'])}")
            print(f"⏱️  Execution Time: {result['execution_time_ms']:.2f}ms")
            print(f"\n💬 Response:")
            print(f"{result['response']}")
            print(f"\n{'='*80}\n")
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"{response.text}")
            return None
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        url = f"{self.base_url}/health"
        response = requests.get(url)
        return response.json()
    
    def list_agents(self) -> Dict[str, Any]:
        """List available agents and their capabilities"""
        url = f"{self.base_url}/agents"
        response = requests.get(url)
        return response.json()


def demo_scenario_1_single_agent():
    """
    Scenario 1: Simple Query - Single Agent (Upstream)
    Menanyakan data produksi dari satu blok
    """
    print("\n" + "="*80)
    print("SCENARIO 1: Single Agent Query - Production Data")
    print("="*80)
    
    client = XYZAIClient()
    
    # Check if API is running
    try:
        health = client.health_check()
        print(f"✅ API Status: {health['status']}")
        print(f"📦 Available Agents: {', '.join(health['agents_available'])}\n")
    except Exception as e:
        print(f"❌ API not running. Please start with: python main.py")
        return
    
    # Query 1: Production data
    client.query(
        query="What is the current oil production in Rokan block?",
        user_id="manager_upstream"
    )
    
    # Query 2: Well status
    client.query(
        query="Check the status of wells in Mahakam block",
        user_id="manager_upstream"
    )
    
    # Query 3: Lifting schedule
    client.query(
        query="When is the next lifting scheduled for Cepu block?",
        user_id="logistics_coordinator"
    )


def demo_scenario_2_logistics():
    """
    Scenario 2: Logistics Queries
    Tracking kapal dan kondisi cuaca
    """
    print("\n" + "="*80)
    print("SCENARIO 2: Logistics Agent - Vessel Tracking")
    print("="*80)
    
    client = XYZAIClient()
    
    # Query 1: Vessel tracking
    client.query(
        query="Where is MT XYZ Prime right now?",
        user_id="logistics_manager"
    )
    
    # Query 2: Weather forecast
    client.query(
        query="What is the weather forecast for Selat Sunda?",
        user_id="shipping_coordinator"
    )
    
    # Query 3: Delivery status
    client.query(
        query="Check the delivery status for shipment SHP-2026-001",
        user_id="logistics_manager"
    )


def demo_scenario_3_finance():
    """
    Scenario 3: Finance Queries
    Analisis keuangan dan profitabilitas
    """
    print("\n" + "="*80)
    print("SCENARIO 3: Finance Agent - Financial Analysis")
    print("="*80)
    
    client = XYZAIClient()
    
    # Query 1: Revenue calculation
    client.query(
        query="Calculate the revenue from 500,000 barrels of oil at $85 per barrel",
        user_id="finance_analyst",
        user_role="finance"
    )
    
    # Query 2: Operating cost
    client.query(
        query="What are the operating costs for Rokan block with current production?",
        user_id="cost_controller",
        user_role="finance"
    )
    
    # Query 3: Market trends
    client.query(
        query="What are the current market price trends for crude oil?",
        user_id="trading_desk",
        user_role="finance"
    )


def demo_scenario_4_multi_agent():
    """
    Scenario 4: Complex Multi-Agent Queries
    Query yang memerlukan kolaborasi multiple agents
    """
    print("\n" + "="*80)
    print("SCENARIO 4: Multi-Agent Collaboration")
    print("="*80)
    
    client = XYZAIClient()
    
    # Query 1: Upstream + Logistics
    client.query(
        query="What is the production in Rokan block and when will it be shipped to Balongan?",
        user_id="operations_manager"
    )
    
    # Query 2: Upstream + Finance
    client.query(
        query="How much revenue can we expect from current Mahakam production?",
        user_id="business_analyst"
    )
    
    # Query 3: All agents
    client.query(
        query="Analyze the profitability of Rokan block considering current production levels and shipping delays due to weather",
        user_id="vp_operations",
        user_role="admin"
    )
    
    # Query 4: Complex business question
    client.query(
        query="Compare the profitability of Rokan vs Cepu blocks, factoring in production volumes, shipping costs, and current oil prices",
        user_id="cfo",
        user_role="admin"
    )


def demo_scenario_5_edge_cases():
    """
    Scenario 5: Edge Cases & Error Handling
    Testing sistem dengan various edge cases
    """
    print("\n" + "="*80)
    print("SCENARIO 5: Edge Cases & Error Handling")
    print("="*80)
    
    client = XYZAIClient()
    
    # Query 1: Ambiguous query
    client.query(
        query="Tell me about XYZ",
        user_id="guest_user"
    )
    
    # Query 2: Unknown block
    client.query(
        query="What is the production in ABC block?",
        user_id="analyst"
    )
    
    # Query 3: Mixed domain
    client.query(
        query="Is there any relationship between weather conditions and oil prices?",
        user_id="researcher"
    )


def demo_full_workflow():
    """
    Demo complete workflow dari query sederhana hingga kompleks
    """
    print("\n" + "🛢️ "*20)
    print("XYZ AI NEXUS - COMPLETE DEMONSTRATION")
    print("🛢️ "*20)
    
    client = XYZAIClient()
    
    # Step 1: Check system health
    print("\n📋 Step 1: System Health Check")
    print("-" * 80)
    try:
        health = client.health_check()
        print(f"Status: {health['status']}")
        print(f"Version: {health['version']}")
        print(f"Available Agents: {', '.join(health['agents_available'])}")
        
        agents_info = client.list_agents()
        print(f"\nAgent Details:")
        for agent in agents_info['agents']:
            print(f"  • {agent['name']}: {agent['description']}")
    except Exception as e:
        print(f"❌ Error: Cannot connect to API. Please run: python main.py")
        return
    
    # Step 2: Simple queries
    print("\n📋 Step 2: Simple Single-Agent Queries")
    print("-" * 80)
    
    client.query("What is the production in Rokan?")
    client.query("Where is MT XYZ Prime?")
    client.query("Calculate revenue from 300k barrels at $85")
    
    # Step 3: Multi-agent queries
    print("\n📋 Step 3: Complex Multi-Agent Queries")
    print("-" * 80)
    
    client.query(
        "What's the status of Rokan production and its shipment to Balongan, "
        "and how does the weather affect delivery time?"
    )
    
    client.query(
        "Analyze the complete supply chain for Mahakam block: "
        "production volumes, shipping schedule, delivery timeline, "
        "and expected revenue"
    )
    
    print("\n✅ Demo completed successfully!")
    print("\n" + "🛢️ "*20 + "\n")


def interactive_mode():
    """
    Interactive mode - user dapat input query sendiri
    """
    print("\n" + "="*80)
    print("INTERACTIVE MODE - XYZ AI Nexus")
    print("="*80)
    print("\nType your questions. Type 'quit' or 'exit' to stop.\n")
    
    client = XYZAIClient()
    
    # Check health
    try:
        health = client.health_check()
        print(f"✅ Connected to API - Status: {health['status']}\n")
    except Exception as e:
        print(f"❌ Cannot connect to API. Please run: python main.py")
        return
    
    while True:
        try:
            query = input("\n🔍 Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                continue
            
            client.query(query)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "interactive" or mode == "i":
            interactive_mode()
        elif mode == "scenario1":
            demo_scenario_1_single_agent()
        elif mode == "scenario2":
            demo_scenario_2_logistics()
        elif mode == "scenario3":
            demo_scenario_3_finance()
        elif mode == "scenario4":
            demo_scenario_4_multi_agent()
        elif mode == "scenario5":
            demo_scenario_5_edge_cases()
        elif mode == "full":
            demo_full_workflow()
        else:
            print(f"Unknown mode: {mode}")
            print("\nAvailable modes:")
            print("  python examples/demo.py interactive")
            print("  python examples/demo.py scenario1")
            print("  python examples/demo.py scenario2")
            print("  python examples/demo.py scenario3")
            print("  python examples/demo.py scenario4")
            print("  python examples/demo.py scenario5")
            print("  python examples/demo.py full")
    else:
        # Default: run full demo
        demo_full_workflow()


if __name__ == "__main__":
    main()
