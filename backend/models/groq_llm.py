from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Optional
import requests
import time
from config.config import Config


class GroqLLM(LLM):
    """Custom LangChain LLM wrapper for Groq API"""
    
    api_key: str = str(Config.GROQ_API_KEY)
    api_base: str = Config.GROQ_API_BASE
    model: str = Config.GROQ_MODEL
    temperature: float = 0.7
    max_tokens: int = 1024
    max_retries: int = 3
    
    @property
    def _llm_type(self) -> str:
        return "groq"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the Groq API with retry logic"""
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
        
        # Retry logic with exponential backoff
        for attempt in range(self.max_retries):
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
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Rate limit
                    if attempt < self.max_retries - 1:
                        wait_time = (2 ** attempt) * 1  # 1s, 2s, 4s
                        print(f"Rate limit hit. Waiting {wait_time}s before retry {attempt + 1}/{self.max_retries}")
                        time.sleep(wait_time)
                        continue
                    else:
                        return "I'm experiencing high API usage right now. Please try again in a moment, or rephrase your question more simply."
                else:
                    return f"Error calling Groq API: {str(e)}"
                    
            except Exception as e:
                return f"Error calling Groq API: {str(e)}"
        
        return "Unable to process request after multiple attempts. Please try again."
    
    @property
    def _identifying_params(self) -> dict:
        """Get identifying parameters"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }