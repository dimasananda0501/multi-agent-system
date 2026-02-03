
from src.orchestrator.orchestrator import OrchestratorAgent
import os

def visualize_graph():
    orchestrator = OrchestratorAgent()
    graph = orchestrator.build_graph().compile()
    
    # Generate mermaid diagram
    try:
        mermaid_png = graph.get_graph().draw_mermaid_png()
        with open("graph_visualization.png", "wb") as f:
            f.write(mermaid_png)
        print("✅ Graph visualization saved to graph_visualization.png")
    except Exception as e:
        print(f"❌ Error generating PNG visualization: {e}")
        print("Note: You might need to install graphviz (dot) and pygraphviz/pydot for PNG export.")
        
        # Fallback to mermaid text
        print("\n--- Mermaid Diagram (copy to mermaid.live) ---")
        print(graph.get_graph().draw_mermaid())
        print("----------------------------------------------")

if __name__ == "__main__":
    visualize_graph()
