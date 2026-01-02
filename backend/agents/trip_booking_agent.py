from agents.base_agent import BaseAgent
from langchain_core.tools import Tool
from typing import List


class TripBookingAgent(BaseAgent):
    """Trip Booking Agent for hotels, flights, and restaurants"""
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for booking trips"""
        
        def search_flights(details: str) -> str:
            """Search for flights - placeholder"""
            return f"Searching flights: {details}"
        
        def book_flight(details: str) -> str:
            """Book a flight - placeholder"""
            return f"Flight booking processed: {details}"
        
        def search_hotels(details: str) -> str:
            """Search for hotels - placeholder"""
            return f"Searching hotels: {details}"
        
        def book_hotel(details: str) -> str:
            """Book a hotel - placeholder"""
            return f"Hotel booking processed: {details}"
        
        def book_restaurant(details: str) -> str:
            """Book a restaurant - placeholder"""
            return f"Restaurant reservation processed: {details}"
        
        return [
            Tool(
                name="SearchFlights",
                func=search_flights,
                description="Search for available flights based on origin, destination, and dates"
            ),
            Tool(
                name="BookFlight",
                func=book_flight,
                description="Book a flight with specified details"
            ),
            Tool(
                name="SearchHotels",
                func=search_hotels,
                description="Search for available hotels in a location"
            ),
            Tool(
                name="BookHotel",
                func=book_hotel,
                description="Book a hotel room with specified details"
            ),
            Tool(
                name="BookRestaurant",
                func=book_restaurant,
                description="Make a restaurant reservation at the destination"
            )
        ]
    
    def get_prompt_template(self) -> str:
        return """You are a travel booking assistant that helps users plan and book complete trips including flights, hotels, and restaurant reservations.

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