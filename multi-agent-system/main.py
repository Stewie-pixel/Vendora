from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
