from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class AgentConfig(BaseModel):
    name: str
    role: str
    goal: str
    tools: List[str] = []

class BaseAgent(ABC):
    def __init__(self, config: AgentConfig):
        self.config = config
        self.history: List[Dict[str, Any]] = []

    @abstractmethod
    async def process(self, input_data: str) -> str:
        """Process the input and return a response."""
        pass

    def add_memory(self, user_input: str, response: str):
        self.history.append({"input": user_input, "response": response})
