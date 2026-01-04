from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Optional
import requests
import time
import random
from config.config import Config


class GroqLLM(LLM):
    """Custom LangChain LLM wrapper for Groq API with intelligent rate limiting"""
    
    api_key: str = str(Config.GROQ_API_KEY)
    api_base: str = Config.GROQ_API_BASE
    model: str = Config.GROQ_MODEL
    temperature: float = 0.7
    max_tokens: int = 1024
    max_retries: int = 5  # Increased from 3 to 5
    base_wait_time: float = 1.0
    
    # Track consecutive failures for adaptive behavior
    consecutive_failures: int = 0
    
    @property
    def _llm_type(self) -> str:
        return "groq"
    
    def _calculate_wait_time(self, attempt: int) -> float:
        """
        Calculate wait time with exponential backoff and jitter
        
        Args:
            attempt: Current retry attempt (0-indexed)
            
        Returns:
            Wait time in seconds
        """
        # Exponential backoff: 1s, 2s, 4s, 8s, 16s
        exponential_wait = self.base_wait_time * (2 ** attempt)
        
        # Add jitter (random 0-20% variation) to prevent thundering herd
        jitter = exponential_wait * random.uniform(0, 0.2)
        
        # Cap at 30 seconds max
        total_wait = min(exponential_wait + jitter, 30)
        
        # Add extra delay if we've had many consecutive failures
        if self.consecutive_failures > 5:
            total_wait *= 1.5  # 50% longer wait
        
        return total_wait
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the Groq API with intelligent retry logic"""
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
        
        # Retry logic with smart exponential backoff
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
                
                # Success! Reset consecutive failures counter
                self.consecutive_failures = 0
                
                return result["choices"][0]["message"]["content"]
                
            except requests.exceptions.HTTPError as e:
                # Rate limit (429)
                if e.response.status_code == 429:
                    self.consecutive_failures += 1
                    
                    if attempt < self.max_retries - 1:
                        wait_time = self._calculate_wait_time(attempt)
                        print(f"Rate limit hit. Waiting {wait_time:.1f}s before retry {attempt + 1}/{self.max_retries}")
                        if self.consecutive_failures > 3:
                            print(f"Consecutive failures: {self.consecutive_failures} - Adding extra delay")
                        time.sleep(wait_time)
                        continue
                    else:
                        # Final retry failed
                        wait_suggestion = int(self._calculate_wait_time(attempt))
                        return f"Rate limit exceeded after {self.max_retries} attempts. Please wait {wait_suggestion} seconds and try again."
                
                # Server errors (500, 502, 503)
                elif e.response.status_code in [500, 502, 503]:
                    self.consecutive_failures += 1
                    
                    if attempt < self.max_retries - 1:
                        wait_time = self._calculate_wait_time(attempt)
                        print(f"Server error ({e.response.status_code}). Retrying in {wait_time:.1f}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        return "Server is experiencing issues. Please try again in a moment."
                
                # Other HTTP errors
                else:
                    return f"API error ({e.response.status_code}). Please try rephrasing your request."
            
            except requests.exceptions.Timeout:
                self.consecutive_failures += 1
                
                if attempt < self.max_retries - 1:
                    wait_time = self._calculate_wait_time(attempt)
                    print(f"Request timeout. Retrying in {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    return "Request timed out. Please try a simpler request."
            
            except requests.exceptions.ConnectionError:
                self.consecutive_failures += 1
                
                if attempt < self.max_retries - 1:
                    wait_time = self._calculate_wait_time(attempt)
                    print(f"🔌 Connection error. Retrying in {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    return "Unable to connect to API. Please check your connection."
            
            except Exception as e:
                # Unexpected errors - don't retry
                print(f"Unexpected error: {str(e)}")
                return "An unexpected error occurred. Please try again."
        
        # Should never reach here, but just in case
        return "Unable to process request after multiple attempts. Please try again later."
    
    @property
    def _identifying_params(self) -> dict:
        """Get identifying parameters"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "max_retries": self.max_retries
        }
    
    def reset_failure_count(self):
        """Manually reset consecutive failure counter"""
        self.consecutive_failures = 0
        print("Failure counter reset")