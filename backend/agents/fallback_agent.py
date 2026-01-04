from agents.base_agent import BaseAgent
from langchain_core.tools import Tool
from typing import List


class FallbackAgent(BaseAgent):
    """Fallback Agent for non-travel related queries"""
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for fallback responses"""
        
        def get_capabilities(query: str = "") -> str:
            """Return what the travel assistant can help with"""
            return """
I'm specialized in travel assistance. I can help you with:

✈️ Flight Bookings - Book one-way or round-trip flights
🏨 Hotel Reservations - Find and book accommodations  
🍽️ Restaurant Reservations - Reserve dining experiences
🗺️ Complete Trip Planning - Book flights, hotels, and restaurants together
ℹ️ Travel Information - Destinations, weather, travel tips, recommendations

Please ask me about any of these travel-related topics!
"""
        
        return [
            Tool(
                name="GetCapabilities",
                func=get_capabilities,
                description="Get information about what the travel assistant can help with"
            )
        ]
    
    def get_prompt_template(self) -> str:
        return """You are a polite redirect assistant for a travel booking system.

Your job is to kindly let users know this assistant is for TRAVEL tasks only.

When users ask non-travel questions:
1. Acknowledge their question politely
2. Explain you're a travel assistant
3. Redirect them to travel topics

IMPORTANT: You DON'T need to use the GetCapabilities tool. Just respond directly with Final Answer.

EXAMPLES:

User: "What's 2 + 2?"
Thought: This is a math question, not travel. I'll politely redirect.
Final Answer: I appreciate your question! However, I'm a specialized travel assistant focused on helping with flight bookings, hotel reservations, restaurant reservations, and trip planning. I'm not able to help with math questions. Is there anything travel-related I can assist you with today?

User: "How many fins does a dolphin have?"
Thought: Marine biology question, not travel. Politely redirect.
Final Answer: That's an interesting question about marine life! However, I'm specifically designed to help with travel needs like booking flights, hotels, and restaurants, or planning complete trips. For questions about dolphins and marine biology, you'd need a different assistant. Would you like help planning a trip instead?

User: "Write me a poem"
Thought: Creative writing request, not travel. Politely redirect.
Final Answer: I'd love to help, but I'm a travel assistant specialized in flight bookings, hotel reservations, restaurant reservations, and trip planning. I'm not equipped to write poetry. However, if you're planning a trip somewhere, I'd be happy to help with all your travel arrangements!

Keep responses brief (2-3 sentences) and always offer to help with travel instead.

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