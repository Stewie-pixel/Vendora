import os
from google import genai
import openai
import json

class LLMClient:
    def __init__(self, provider="openai"):
        self.provider = provider
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        self.gemini_client = None
        self.openai_client = None

        if self.gemini_key:
            self.gemini_client = genai.Client(api_key=self.gemini_key)
        else:
             print("Warning: GEMINI_API_KEY not found.")

        if self.openai_key:
            self.openai_client = openai.OpenAI(api_key=self.openai_key)
        else:
             print("Warning: OPENAI_API_KEY not found.")

    def complete(self, prompt: str, system_instruction: str = None) -> str:
        """
        Call the configured LLM provider to generate a response.
        """
        # Default system prompt if not checking for "Get Answer" specific logic
        if not system_instruction:
             system_instruction = (
                "You are the Root Agent of a hierarchical system. "
                "Your goal is to parse user queries and decide if a tool is needed. "
                "Output ONLY JSON. "
                "Available tools: get_answer(entity: str). "
                "If the user asks for the answer of a question, output: "
                '{"tool": "get_answer", "args": {"entity": "Question"}}. '
                "Otherwise, output: "
                '{"message": "Your response here"}.'
            )

        if self.provider == "openai":
            if not self.openai_client:
                return '{"message": "OpenAI API Key missing."}'
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                return response.choices[0].message.content
            except Exception as e:
                return json.dumps({"message": f"Error calling OpenAI: {str(e)}"})

        elif self.provider == "gemini":
            if not self.gemini_client:
                return '{"message": "Gemini API Key missing."}'
            try:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=f"{system_instruction}\nUser Query: {prompt}"
                )
                return response.text.strip()
            except Exception as e:
                return json.dumps({"message": f"Error calling Gemini: {str(e)}"})
        
        return '{"message": "Invalid provider specified."}'

