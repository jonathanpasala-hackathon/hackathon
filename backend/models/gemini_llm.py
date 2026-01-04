"""
Gemini LLM implementation with LangChain compatibility
"""
from config.config import Config
import time
from typing import Optional, List, Any, Mapping
import google.generativeai as genai
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun


class GeminiLLM(LLM):
    """LangChain-compatible wrapper for Google Gemini API with rate limiting"""
    
    model_name: str = Config.GEMINI_MODEL
    max_retries: int = 3
    temperature: float = 0.7
    top_p: float = 0.95
    top_k: int = 40
    max_output_tokens: int = 8192
    
    def __init__(self, **kwargs):
        """Initialize Gemini LLM"""
        super().__init__(**kwargs)
        
        # Configure Gemini API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)
        
        # Generation config
        self.generation_config = {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "max_output_tokens": self.max_output_tokens,
        }
    
    @property
    def _llm_type(self) -> str:
        """Return LLM type identifier"""
        return "gemini"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Call Gemini API with rate limiting and retries
        
        Args:
            prompt: Input prompt
            stop: Stop sequences (optional)
            run_manager: Callback manager (optional)
            
        Returns:
            Generated text response
        """
        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_config
                )
                
                # Return the text response
                return response.text
                
            except Exception as e:
                error_msg = str(e).lower()
                
                # Handle rate limiting
                if 'rate limit' in error_msg or 'quota' in error_msg or '429' in error_msg:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    print(f"Rate limit hit. Waiting {wait_time}s before retry {attempt + 1}/{self.max_retries}")
                    time.sleep(wait_time)
                    continue
                
                # Handle safety filters
                elif 'safety' in error_msg:
                    return "I apologize, but I cannot generate that response due to safety guidelines."
                
                else:
                    # Re-raise unexpected errors
                    raise e
        
        # If all retries failed
        raise Exception("I'm experiencing high API usage right now. Please try again in a moment, or rephrase your question more simply.")
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters"""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "max_output_tokens": self.max_output_tokens,
        }