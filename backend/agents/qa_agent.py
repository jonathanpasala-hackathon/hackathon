from agents.base_agent import BaseAgent
from langchain_core.tools import Tool
from typing import List


class QAAgent(BaseAgent):
    """Travel Question and Answer Agent"""
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for travel Q&A"""
        
        def search_knowledge(query: str) -> str:
            """Search knowledge base for travel information - placeholder for now"""
            return f"Searching for travel information about: {query}. This is a placeholder response."
        
        return [
            Tool(
                name="SearchKnowledge",
                func=search_knowledge,
                description="Search the travel knowledge base for information about destinations, weather, tips, and recommendations"
            )
        ]
    
    def get_prompt_template(self) -> str:
        return """You are a helpful travel information assistant specializing in destinations, travel tips, weather, and recommendations.

Answer travel-related questions to the best of your ability. Provide helpful information about:
- Destinations and attractions
- Weather and best times to visit
- Travel tips and advice  
- Cultural information
- Local customs and etiquette
- Transportation options
- General travel recommendations

Use the available tools if needed to search for current information.

You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought: {agent_scratchpad}"""