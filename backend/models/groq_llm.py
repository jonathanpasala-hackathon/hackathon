from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Optional
import requests
from config.config import Config


class GroqLLM(LLM):
    """Custom LangChain LLM wrapper for Grok API"""
    
    api_key: str = str(Config.GROQ_API_KEY)
    api_base: str = Config.GROQ_API_BASE
    model: str = Config.GROQ_MODEL
    temperature: float = 0.7
    max_tokens: int = 1024
    
    @property
    def _llm_type(self) -> str:
        return "grok"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the Grok API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False
        }
        
        if stop:
            payload["stop"] = stop
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error calling Grok API: {str(e)}"
    
    @property
    def _identifying_params(self) -> dict:
        """Get identifying parameters"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }