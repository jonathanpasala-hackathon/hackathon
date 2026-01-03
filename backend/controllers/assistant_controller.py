from models.agent_router import AgentRouter
from typing import Dict, Any


class AssistantController:
    """Main controller for the personal assistant"""
    
    def __init__(self):
        self.router = AgentRouter()
        # Store conversation history by session (in production, use proper session management)
        self.conversations = {}
    
    def process_request(self, user_input: str, session_id: str = "default") -> Dict[str, Any]:
        """Process user request and return formatted response"""
        
        if not user_input or not user_input.strip():
            return {
                "success": False,
                "agent": None,
                "response": "Please provide a valid input.",
                "error": "Empty input"
            }
        
        try:
            # Get or create conversation history for this session
            if session_id not in self.conversations:
                self.conversations[session_id] = {
                    "history": [],
                    "current_agent": None,
                    "collected_data": {}
                }
            
            conversation = self.conversations[session_id]
            
            # Build context from conversation history
            context = self._build_context(conversation["history"], user_input)
            
            # Route with context
            result = self.router.route(context, conversation.get("current_agent"))
            
            # Update conversation history
            conversation["history"].append({
                "user": user_input,
                "agent": result["agent"],
                "response": result["response"]
            })
            conversation["current_agent"] = result["agent"]
            
            return result
        except Exception as e:
            return {
                "success": False,
                "agent": None,
                "response": "An error occurred processing your request.",
                "error": str(e)
            }
    
    def _build_context(self, history: list, current_input: str) -> str:
        """Build context string from conversation history"""
        if not history:
            return current_input
        
        # Include last few messages for context
        context_parts = []
        for msg in history[-3:]:  # Last 3 exchanges
            context_parts.append(f"User: {msg['user']}")
            context_parts.append(f"Assistant: {msg['response']}")
        
        context_parts.append(f"User: {current_input}")
        
        return "\n".join(context_parts)
    
    def clear_conversation(self, session_id: str = "default"):
        """Clear conversation history for a session"""
        if session_id in self.conversations:
            del self.conversations[session_id]
    
    def get_agent_info(self) -> Dict[str, str]:
        """Get information about available agents"""
        return {
            "qa": "Travel Q&A - Ask about destinations, weather, travel tips, and recommendations!",
            "reservation": "Individual Reservations - Book hotels, restaurants, or flights one at a time",
            "trip_booking": "Complete Trip Planning - Book entire trips with flights, hotels, and dining"
        }