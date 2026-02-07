from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
import os

# Load env vars first

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", ".env")
load_dotenv(env_path)

from agents.root.root_agent import RootAgent

app = FastAPI(title="Vendora Multi-Agent System")
root_agent = RootAgent()

class UserRequest(BaseModel):
    query: str

@app.post("/api/request")
async def process_request(request: UserRequest):
    """
    Entry point for User -> RootAgent
    """
    try:
        # TODO: Implement actual run logic in RootAgent
        response = root_agent.run(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import argparse
    import uvicorn
    import sys
    
    parser = argparse.ArgumentParser(description="Run Vendora Cookbook Agent")
    parser.add_argument("--query", type=str, help="Direct query to run against the Root Agent")
    parser.add_argument("--server", action="store_true", help="Start the API server")
    parser.add_argument("--provider", type=str, choices=["openai", "gemini"], help="Specific provider to use (overrides auto-detect)")
    
    args = parser.parse_args()

    if args.query:
        # Run in CLI mode
        # Create a new agent instance to respect CLI args (ignoring global instance default)
        # Note: We need to import RootAgent locally if not imported, but it is imported at top level.
        cli_agent = RootAgent(provider=args.provider)
        
        print(f"User Query: {args.query}")
        print(f"Provider: {cli_agent.llm.provider}")
        try:
            response = cli_agent.run(args.query)
            print(f"Agent Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
            
    elif args.server:
        # Run server mode
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        # Default to server if no args (or print help)
        # For backward compatibility with "python main.py", let's default to server
        print("No arguments provided. Starting server... (Use --query 'Your question' for CLI mode)")
        uvicorn.run(app, host="0.0.0.0", port=8000)
