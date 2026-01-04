from agents.base_agent import BaseAgent
from langchain_core.tools import Tool
from typing import List, Dict, Any
from tools.data_display_tool import DataDisplayTool
import json
import re
from datetime import datetime, timedelta


class EnhancedReservationAgent(BaseAgent):
    """Enhanced Reservation Agent with conversational flow"""
    
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.reservation_state = {
            "type": None,
            "collected_info": {}
        }
        super().__init__()
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for making reservations"""
        
        display_tool = DataDisplayTool.create_display_tool(self.session_id)
        
        def confirm_reservation(details_json: str) -> str:
            """Confirm a reservation after all info is collected"""
            try:
                details = json.loads(details_json)
                res_type = details.get("type", "").lower()
                
                import random
                conf_num = f"{res_type.upper()[:3]}-{random.randint(100000, 999999)}"
                
                if res_type == "hotel":
                    message = f"""✅ Hotel Reservation Confirmed!
Confirmation: {conf_num}
Hotel: {details.get('city', 'N/A')}
Guests: {details.get('people', 'N/A')}
Check-in: {details.get('checkin', 'N/A')}
Check-out: {details.get('checkout', 'N/A')}
Name: {details.get('name', 'N/A')}"""
                
                elif res_type == "restaurant":
                    message = f"""✅ Restaurant Reservation Confirmed!
Confirmation: {conf_num}
Location: {details.get('city', 'N/A')}
Party Size: {details.get('people', 'N/A')}
Date: {details.get('date', 'N/A')}
Time: {details.get('time', 'N/A')}
Name: {details.get('name', 'N/A')}"""
                
                elif res_type == "flight":
                    message = f"""✅ Flight Reservation Confirmed!
Confirmation: {conf_num}
Tickets: {details.get('tickets', 'N/A')}
Route: {details.get('from', 'N/A')} → {details.get('to', 'N/A')}
Departure: {details.get('departure_date', 'N/A')}
Type: {details.get('trip_type', 'N/A')}
Name: {details.get('name', 'N/A')}"""
                
                else:
                    message = f"✅ Reservation Confirmed! Confirmation: {conf_num}"
                
                return message
                
            except Exception as e:
                return f"Error confirming reservation: {str(e)}"
        
        return [display_tool, Tool(
            name="ConfirmReservation",
            func=confirm_reservation,
            description="Confirm a reservation after collecting all required information"
        )]
    
    def get_prompt_template(self) -> str:
        return """You are a friendly reservation specialist who makes booking easy through natural conversation.

You help book hotels, restaurants, and flights by having casual, flowing conversations.

WHAT YOU NEED (but gather naturally):
Hotels: city, number of people, check-in/out dates, name
Restaurants: city, number of people, date, time, name  
Flights: tickets, from/to cities, dates, round trip?, name

CONVERSATION STYLE:

Bad (robotic):
User: "book a hotel"
You: "What is the city?"
User: "NYC"
You: "What is the number of people?"

Good (natural):
User: "book a hotel"
You: "I'd love to help! Where are you heading and when?"
User: "NYC next month with my wife"
You: "Perfect! NYC is great. What dates work for you two?"

UNDERSTAND CASUAL LANGUAGE:
- "me and my partner" = 2 people
- "next Tuesday" = calculate the actual date
- "for 3 nights" = calculate checkout from checkin
- "around 7" or "dinner time" = 7:00 PM
- "something cheap" = use max_price filter ~$100
- "nice place" = max_price ~$300
- "show me options" = use DisplayResults

ASKING QUESTIONS (NO ACTION NEEDED):
User: "I need a restaurant reservation in new york"
Thought: User wants restaurant in NYC. Need to ask how many people.
Final Answer: I'd love to help you with that! How many people are you planning to dine with in New York, and do you have a specific date in mind?

User: "4 people"
Thought: Got people=4. Need date next.
Final Answer: Great! What date would you like to dine? (Format: YYYY-MM-DD)

SHOWING OPTIONS (use DisplayResults anytime):
When they want to see hotels/restaurants/flights:
Action: DisplayResults
Action Input: {{"type": "hotels", "filters": {{"city": "New York", "max_price": 150}}}}

CONFIRMING (when you have everything):
User: "Jon"
Thought: I have all info. Time to confirm.
Action: ConfirmReservation
Action Input: {{"type": "restaurant", "city": "NYC", "people": "4", "date": "2026-01-08", "time": "20:00", "name": "Jon"}}
Observation: ✅ Restaurant Reservation Confirmed! Confirmation: RES-123456...
Thought: Got the confirmation! Now return it to the user.
Final Answer: ✅ Restaurant Reservation Confirmed! Confirmation: RES-123456
Location: New York
Party Size: 4
Date: 2026-01-08
Time: 20:00
Name: Jon

REMEMBER CONTEXT:
If they mentioned "NYC" earlier, you remember it.
If they're booking a hotel Feb 15-18, suggest restaurant dates in that range.

CRITICAL: When asking questions, skip straight to Final Answer - DO NOT write "Action: None"!

Be warm, natural, and helpful. Don't interrogate - have a conversation!

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

REMEMBER: Only use Action when calling a tool. When asking questions, go straight to Final Answer!
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}"""