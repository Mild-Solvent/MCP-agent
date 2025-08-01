#!/usr/bin/env python3
"""
MCP Google Analytics Agent - Main Runner

This script provides a convenient way to start either the MCP server
or the AI agent, or both components together.

Usage:
    python main.py server      # Start MCP server only
    python main.py agent       # Start agent only (requires server to be running)
    python main.py both        # Start both server and agent
    python main.py interactive # Start agent in interactive mode
"""

import sys
import asyncio
import subprocess
import time
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def start_server():
    """Start the MCP server in a subprocess."""
    print("🚀 Starting MCP Server...")
    server_script = Path(__file__).parent / "src" / "mcp_server" / "ga_mcp_server.py"
    return subprocess.Popen([sys.executable, str(server_script)])

async def start_agent(mode="analyze"):
    """Start the AI agent."""
    print("🤖 Starting Analytics Agent...")
    from agent.analytics_agent import AnalyticsAgent
    
    agent = AnalyticsAgent()
    
    try:
        await agent.initialize()
        
        if mode == "interactive":
            # Interactive mode
            print("\n🤖 Analytics Agent - Interactive Mode")
            print("Ask me questions about your website analytics!")
            print("Type 'analyze' for a full report, or 'quit' to exit.\n")
            
            while True:
                try:
                    question = input("❓ Your question: ").strip()
                    if question.lower() in ['quit', 'exit', 'q']:
                        break
                    elif question.lower() == 'analyze':
                        report = await agent.run_comprehensive_analysis()
                        print("\n" + report + "\n")
                    elif question:
                        answer = await agent.answer_question(question)
                        print(f"🤖 {answer}\n")
                except KeyboardInterrupt:
                    break
            
            print("👋 Goodbye!")
        
        else:
            # Analysis mode
            report = await agent.run_comprehensive_analysis()
            print("\n" + report)
    
    finally:
        await agent.close()

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python main.py [server|agent|both|interactive]")
        print("\nOptions:")
        print("  server      - Start MCP server only")
        print("  agent       - Start agent only (server must be running)")
        print("  both        - Start both server and agent")
        print("  interactive - Start agent in interactive Q&A mode")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == "server":
        # Start server only
        try:
            server_process = start_server()
            print("✅ MCP Server started. Press Ctrl+C to stop.")
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            server_process.terminate()
    
    elif mode == "agent":
        # Start agent only
        asyncio.run(start_agent("analyze"))
    
    elif mode == "interactive":
        # Start agent in interactive mode
        asyncio.run(start_agent("interactive"))
    
    elif mode == "both":
        # Start both server and agent
        server_process = None
        try:
            # Start server
            server_process = start_server()
            print("⏳ Waiting for server to start...")
            time.sleep(3)  # Give server time to start
            
            # Start agent
            print("🤖 Starting agent...")
            asyncio.run(start_agent("analyze"))
            
        except KeyboardInterrupt:
            print("\n🛑 Stopping...")
        finally:
            if server_process:
                server_process.terminate()
    
    else:
        print(f"Unknown mode: {mode}")
        print("Use: server, agent, both, or interactive")
        sys.exit(1)

if __name__ == "__main__":
    main()
