from agents.base_agent import BaseAgent
from langchain_core.tools import Tool
from typing import List


class QAAgent(BaseAgent):
    """Question and Answer Agent"""
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for QA"""
        
        def search_knowledge(query: str) -> str:
            """Search knowledge base - placeholder for now"""
            return f"Searching for: {query}. This is a placeholder response."
        
        return [
            Tool(
                name="SearchKnowledge",
                func=search_knowledge,
                description="Search the knowledge base for information to answer questions"
            )
        ]
    
    def get_prompt_template(self) -> str:
        return """You are a helpful question-answering assistant.
        
Answer the following question to the best of your ability. Use the available tools if needed.

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