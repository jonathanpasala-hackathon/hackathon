from agents.base_agent import BaseAgent
from langchain_core.tools import Tool
from typing import List


class EmailSummarizerAgent(BaseAgent):
    """Email Summarization Agent"""
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for email summarization"""
        
        def fetch_emails(criteria: str) -> str:
            """Fetch emails based on criteria - placeholder"""
            return f"Fetching emails: {criteria}"
        
        def summarize_email(email_id: str) -> str:
            """Summarize a specific email - placeholder"""
            return f"Summary for email {email_id}: This is a placeholder summary."
        
        def categorize_emails(email_list: str) -> str:
            """Categorize emails - placeholder"""
            return f"Categorizing emails: {email_list}"
        
        return [
            Tool(
                name="FetchEmails",
                func=fetch_emails,
                description="Fetch emails based on criteria (unread, from specific sender, date range, etc.)"
            ),
            Tool(
                name="SummarizeEmail",
                func=summarize_email,
                description="Generate a summary of a specific email"
            ),
            Tool(
                name="CategorizeEmails",
                func=categorize_emails,
                description="Categorize emails by importance, topic, or sender"
            )
        ]
    
    def get_prompt_template(self) -> str:
        return """You are an email summarization assistant that helps users understand and manage their emails efficiently.

You have access to the following tools:
{tools}

Use the following format:

Question: the input question or request
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought: {agent_scratchpad}"""