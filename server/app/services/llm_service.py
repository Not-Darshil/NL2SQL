import httpx
import json
from typing import List, Dict, Any, Optional
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.url = f"{settings.OLLAMA_URL}/api/generate"
        self.model = settings.OLLAMA_MODEL

    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        """
        Calls Ollama API to generate a response.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(self.url, json=payload)
                response.raise_for_status()
                
                result = response.json()
                return result.get("response", "")
            except httpx.HTTPStatusError as e:
                # Log error or handle specifically
                return f"LLM Error: {str(e)}"
            except Exception as e:
                return f"Unexpected Error: {str(e)}"

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        """
        Calls Ollama Chat API.
        """
        url = f"{settings.OLLAMA_URL}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": temperature
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                
                result = response.json()
                return result.get("message", {}).get("content", "")
            except Exception as e:
                return f"Chat Error: {str(e)}"

llm_service = LLMService()
