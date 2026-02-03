from typing import Dict, List
from .agents.core import BaseAgent, AgentConfig

class Orchestrator:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent):
        self.agents[agent.config.name] = agent

    def get_agent(self, name: str) -> BaseAgent:
        return self.agents.get(name)

    def list_agents(self) -> List[str]:
        return list(self.agents.keys())
