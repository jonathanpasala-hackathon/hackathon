from models.agent_router import AgentRouter
from typing import Dict, Any


class AssistantController:
    """Main controller for the personal assistant"""
    
    def __init__(self):
        self.router = AgentRouter()
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process user request and return formatted response"""
        
        if not user_input or not user_input.strip():
            return {
                "success": False,
                "agent": None,
                "response": "Please provide a valid input.",
                "error": "Empty input"
            }
        
        try:
            result = self.router.route(user_input)
            return result
        except Exception as e:
            return {
                "success": False,
                "agent": None,
                "response": "An error occurred processing your request.",
                "error": str(e)
            }
    
    def get_agent_info(self) -> Dict[str, str]:
        """Get information about available agents"""
        return {
            "qa": "Question and Answer - Ask me anything!",
            "reservation": "Reservation Assistant - Make restaurant and table reservations",
            "trip_booking": "Trip Booking - Book flights, hotels, and restaurant reservations for your trips",
            "email_summarizer": "Email Summarizer - Summarize and manage your emails"
        }