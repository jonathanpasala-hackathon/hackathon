from abc import ABC, abstractmethod
from models.groq_llm import GroqLLM
from langchain_classic.agents import create_react_agent
from langchain_classic.agents import AgentExecutor
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from typing import List, Dict, Any


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self):
        self.llm = GroqLLM()
        self.tools = self._create_tools()
        self.agent = self._create_agent()
    
    @abstractmethod
    def _create_tools(self) -> List[Tool]:
        """Create tools specific to this agent"""
        pass
    
    @abstractmethod
    def get_prompt_template(self) -> str:
        """Get the prompt template for this agent"""
        pass
    
    def _create_agent(self) -> AgentExecutor:
        """Create the agent executor"""
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
            max_iterations=5
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent with given input"""
        try:
            result = self.agent.invoke(input_data)
            return {
                "success": True,
                "output": result.get("output", ""),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e)
            }