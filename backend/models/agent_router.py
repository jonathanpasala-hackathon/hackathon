from agents.qa_agent import QAAgent
from agents.reservation_agent import EnhancedReservationAgent
from agents.trip_booking_agent import TripBookingAgent
from agents.fallback_agent import FallbackAgent
from models.groq_llm import GroqLLM
from typing import Dict, Any


class AgentRouter:
    """Routes user requests to the appropriate agent"""
    
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.agents = {
            "qa": QAAgent(session_id=session_id),
            "reservation": EnhancedReservationAgent(session_id=session_id),
            "trip_booking": TripBookingAgent(),
            "fallback": FallbackAgent()
        }
        self.llm = GroqLLM()
    
    def _classify_intent(self, user_input: str) -> str:
        """Classify user intent to route to appropriate agent"""
        
        classification_prompt = f"""Classify the following user request into one of these categories:

- reservation: Booking a SINGLE travel item (one hotel, one restaurant, or one flight)
  Examples: "book a hotel", "reserve a restaurant", "book a flight", "I need a hotel in NYC"
  
- trip_booking: Booking a COMPLETE TRIP with multiple items (flight + hotel + restaurant)
  Examples: "plan a trip to Paris", "book my vacation to Hawaii", "I need everything for my trip"
  
- qa: Travel-related questions, information, and recommendations
  Examples: "what's the weather in Paris", "best time to visit Tokyo", "tell me about Rome", "travel tips for Italy"
  
- fallback: NON-TRAVEL questions (math, science, general knowledge, sports, entertainment, coding, etc.)
  Examples: "what's 2+2", "who won the Super Bowl", "write me a poem", "how does photosynthesis work", "help me code"

User request: {user_input}

IMPORTANT: Only classify as qa if the question is SPECIFICALLY about travel/destinations/weather/travel tips.
For ANY non-travel topic, classify as fallback.

Respond with ONLY the category name: reservation, trip_booking, qa, or fallback
"""
        
        try:
            intent = self.llm._call(classification_prompt).strip().lower()
            
            # Validate the intent
            if intent not in self.agents:
                # Default to fallback for unclear queries
                if any(word in user_input.lower() for word in ['hotel', 'flight', 'restaurant', 'book', 'reserve', 'reservation', 'trip', 'travel']):
                    return "reservation"
                return "fallback"
            
            return intent
        except Exception as e:
            print(f"Error classifying intent: {e}")
            return "fallback"  # Default to fallback on errors
    
    def route(self, user_input: str, current_agent: str = None) -> Dict[str, Any]: # type: ignore
        """Route user input to appropriate agent and return response"""
        
        # If we have a current agent in conversation, stick with it unless user explicitly switches
        if current_agent:
            # Check if user is trying to switch topics
            switch_keywords = ["new", "different", "instead", "switch", "change topic"]
            is_switching = any(keyword in user_input.lower() for keyword in switch_keywords)
            
            if not is_switching:
                # Continue with same agent
                print(f"[Router] Continuing with: {current_agent}")
                agent = self.agents.get(current_agent)
                result = agent.execute({"input": user_input}) # type: ignore
                
                return {
                    "agent": current_agent,
                    "success": result["success"],
                    "response": result["output"],
                    "error": result["error"]
                }
        
        # Classify the intent for new conversations
        intent = self._classify_intent(user_input)
        print(f"[Router] Classified intent as: {intent}")
        
        # Get the appropriate agent
        agent = self.agents.get(intent)
        print(f"[Router] Using agent: {agent.__class__.__name__}")
        
        # Execute the agent
        result = agent.execute({"input": user_input}) # type: ignore
        
        return {
            "agent": intent,
            "success": result["success"],
            "response": result["output"],
            "error": result["error"]
        }