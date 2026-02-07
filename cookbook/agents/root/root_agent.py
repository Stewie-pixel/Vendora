import os
import json
from llm.llm_client import LLMClient
from tools.basic import get_answer

class RootAgent:
    def __init__(self, provider=None):
        
        if not provider:
            provider = "openai" # Default fallback

            if os.getenv("OPENAI_API_KEY") and not os.getenv("GEMINI_API_KEY"):
                 provider = "openai"

            elif os.getenv("OPENAI_API_KEY"):
                 provider = "openai"
             
        self.llm = LLMClient(provider=provider)

    def run(self, user_input: str) -> str:
        # 1. Parse user intent using LLM
        llm_response = self.llm.complete(user_input)
        
        try:
            parsed = json.loads(llm_response)
        except json.JSONDecodeError:
            return "Error parsing LLM response."

        # 2. Execute tool if requested
        if "tool" in parsed and parsed["tool"] == "get_answer":
            entity = parsed["args"].get("entity")

            if entity:
                result = get_answer(entity)
                # 3. Return answer directly
                return result
        
        return parsed.get("message", "Could not process request.")

