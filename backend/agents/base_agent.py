from abc import ABC, abstractmethod
from models.groq_llm import GroqLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from typing import List, Dict, Any
import time

# Import agent functionality
from langchain_classic.agents import AgentExecutor, create_react_agent


class BaseAgent(ABC):
    """Base class for all agents with circuit breaker"""
    
    def __init__(self):
        self.llm = GroqLLM()
        self.tools = self._create_tools()
        self.agent = self._create_agent()
        
        # Circuit breaker settings
        self.consecutive_errors = 0
        self.max_consecutive_errors = 3
        self.circuit_open_until = 0
        self.circuit_cooldown = 60  # seconds
    
    @abstractmethod
    def _create_tools(self) -> List[Tool]:
        """Create tools specific to this agent"""
        pass
    
    @abstractmethod
    def get_prompt_template(self) -> str:
        """Get the prompt template for this agent"""
        pass
    
    def _create_agent(self) -> AgentExecutor:
        """Create the agent executor with reasonable limits"""
        prompt = PromptTemplate.from_template(self.get_prompt_template())
        
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=15,  # Reduced from 90 to prevent excessive API calls
            max_execution_time=120,  # 2 minute timeout
            early_stopping_method="generate"
        )
    
    def _check_circuit_breaker(self) -> tuple:
        """Check if circuit breaker is open"""
        current_time = time.time()
        
        if current_time < self.circuit_open_until:
            remaining = int(self.circuit_open_until - current_time)
            return False, f"Too many errors. Please wait {remaining} seconds before trying again."
        
        return True, None
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent with circuit breaker protection"""
        
        # Check circuit breaker
        can_proceed, error_msg = self._check_circuit_breaker()
        if not can_proceed:
            return {
                "success": False,
                "output": None,
                "error": error_msg
            }
        
        try:
            result = self.agent.invoke(input_data)
            
            # Success - reset error counter
            self.consecutive_errors = 0
            
            return {
                "success": True,
                "output": result.get("output", ""),
                "error": None
            }
            
        except Exception as e:
            error_str = str(e).lower()
            
            # Increment error counter
            self.consecutive_errors += 1
            
            # Check if we should open circuit breaker
            if self.consecutive_errors >= self.max_consecutive_errors:
                self.circuit_open_until = time.time() + self.circuit_cooldown
                print(f"Circuit breaker opened! Consecutive errors: {self.consecutive_errors}")
                print(f"Cooling down for {self.circuit_cooldown} seconds...")
                
                return {
                    "success": False,
                    "output": None,
                    "error": f"Too many errors. Please wait {self.circuit_cooldown} seconds and try rephrasing your request."
                }
            
            # Handle rate limiting gracefully
            if 'rate limit' in error_str or '429' in error_str:
                return {
                    "success": False,
                    "output": None,
                    "error": "I'm experiencing high API usage. Please wait a moment and try again."
                }
            
            # Handle iteration limit
            elif 'iteration limit' in error_str or 'max iterations' in error_str:
                return {
                    "success": False,
                    "output": None,
                    "error": "This request is too complex. Please try breaking it into smaller steps."
                }
            
            # Handle timeout
            elif 'timeout' in error_str or 'execution time' in error_str:
                return {
                    "success": False,
                    "output": None,
                    "error": "Request took too long. Please try a simpler request."
                }
            
            # Generic error
            else:
                return {
                    "success": False,
                    "output": None,
                    "error": "An error occurred. Please try rephrasing your request."
                }