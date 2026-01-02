from agents.base_agent import BaseAgent
from langchain_core.tools import Tool
from typing import List


class ReservationAgent(BaseAgent):
    """Restaurant/General Reservation Agent"""
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for making reservations"""
        
        def check_availability(details: str) -> str:
            """Check reservation availability - placeholder"""
            return f"Checking availability for: {details}"
        
        def make_reservation(details: str) -> str:
            """Make a reservation - placeholder"""
            return f"Reservation request processed: {details}"
        
        def cancel_reservation(reservation_id: str) -> str:
            """Cancel a reservation - placeholder"""
            return f"Cancellation request for: {reservation_id}"
        
        return [
            Tool(
                name="CheckAvailability",
                func=check_availability,
                description="Check availability for a reservation (restaurant, table, etc.)"
            ),
            Tool(
                name="MakeReservation",
                func=make_reservation,
                description="Make a reservation with specified details (date, time, party size, location)"
            ),
            Tool(
                name="CancelReservation",
                func=cancel_reservation,
                description="Cancel an existing reservation using reservation ID"
            )
        ]
    
    def get_prompt_template(self) -> str:
        return """You are a reservation assistant that helps users make, check, and cancel reservations.

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