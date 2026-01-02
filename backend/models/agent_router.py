from agents.qa_agent import QAAgent
from agents.reservation_agent import ReservationAgent
from agents.trip_booking_agent import TripBookingAgent
from agents.email_summarizer_agent import EmailSummarizerAgent
from models.groq_llm import GroqLLM
from typing import Dict, Any


class AgentRouter:
    """Routes user requests to the appropriate agent"""
    
    def __init__(self):
        self.agents = {
            "qa": QAAgent(),
            "reservation": ReservationAgent(),
            "trip_booking": TripBookingAgent(),
            "email_summarizer": EmailSummarizerAgent()
        }
        self.llm = GroqLLM()
    
    def _classify_intent(self, user_input: str) -> str:
        """Classify user intent to route to appropriate agent"""
        
        classification_prompt = f"""Classify the following user request into one of these categories:
- qa: General questions and answers
- reservation: Making, checking, or canceling a single reservation (restaurant, etc.)
- trip_booking: Booking complete trips with flights, hotels, and restaurants
- email_summarizer: Summarizing, categorizing, or managing emails

User request: {user_input}

Respond with only the category name (qa, reservation, trip_booking, or email_summarizer).
"""
        
        try:
            intent = self.llm._call(classification_prompt).strip().lower()
            
            # Validate the intent
            if intent not in self.agents:
                # Default to QA if classification is unclear
                return "qa"
            
            return intent
        except Exception as e:
            print(f"Error classifying intent: {e}")
            return "qa"  # Default to QA agent
    
    def route(self, user_input: str) -> Dict[str, Any]:
        """Route user input to appropriate agent and return response"""
        
        # Classify the intent
        intent = self._classify_intent(user_input)
        
        # Get the appropriate agent
        agent = self.agents.get(intent)
        
        # Execute the agent
        result = agent.execute({"input": user_input})  # type: ignore
        
        return {
            "agent": intent,
            "success": result["success"],
            "response": result["output"],
            "error": result["error"]
        }