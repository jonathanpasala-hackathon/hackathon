from agents.base_agent import BaseAgent
from langchain_core.tools import Tool
from typing import List, Dict, Any
from tools.data_display_tool import DataDisplayTool
import json


class EnhancedReservationAgent(BaseAgent):
    """Enhanced Reservation Agent with display data support"""
    
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.reservation_state = {
            "type": None,  # hotel, restaurant, or flight
            "collected_info": {}
        }
        super().__init__()
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for making reservations"""
        
        # Get the display tool
        display_tool = DataDisplayTool.create_display_tool(self.session_id)
        
        def confirm_reservation(details_json: str) -> str:
            """
            Confirm a reservation after all info is collected.
            Input: JSON with type and all collected details
            """
            try:
                details = json.loads(details_json)
                res_type = details.get("type", "").lower()
                
                # Generate confirmation number
                import random
                conf_num = f"{res_type.upper()[:3]}-{random.randint(100000, 999999)}"
                
                # Build confirmation message
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
        
        return [
            display_tool,  # DisplayResults tool
            Tool(
                name="ConfirmReservation",
                func=confirm_reservation,
                description="""Confirm a reservation after collecting all required information. 
                Input: JSON with type (hotel/restaurant/flight) and all collected details.
                Example: '{\"type\": \"hotel\", \"city\": \"NYC\", \"people\": \"2\", \"checkin\": \"2026-02-15\", \"checkout\": \"2026-02-18\", \"name\": \"John Smith\"}'"""
            )
        ]
    
    def get_prompt_template(self) -> str:
        return """You are a reservation assistant that helps users book hotels, restaurants, and flights.

Your workflow:
1. Determine what type of reservation (hotel, restaurant, or flight)
2. If user asks to "show" or "find" options, use DisplayResults to show available options
3. Collect required information one question at a time
4. When you have ALL required info, use ConfirmReservation to complete the booking

IMPORTANT: When user says "show me hotels" or "find restaurants" or asks for options:
- ALWAYS use DisplayResults tool to show visual cards
- Trigger words: "show", "find", "display", "see", "search", "available", "options", "what are", "list"
- Works at ANY point in conversation - beginning, middle, or end
- After showing results, continue with booking questions
- Then proceed with booking conversation

REQUIRED INFORMATION:

HOTEL:
1. City/location
2. Number of people
3. Check-in date (YYYY-MM-DD)
4. Check-out date (YYYY-MM-DD)
5. Name on reservation

RESTAURANT:
1. City/location
2. Number of people
3. Date (YYYY-MM-DD)
4. Time
5. Name on reservation

FLIGHT:
1. Number of tickets
2. Departing city
3. Arriving city
4. Departure date (YYYY-MM-DD)
5. Round trip? (yes/no)
6. Return date (if round trip)
7. Name on reservation

WORKFLOW EXAMPLES:

Example 1 - User asks to see options first:
User: "Show me hotels in NYC"
Thought: User wants to see hotel options. Use DisplayResults.
Action: DisplayResults
Action Input: {{"type": "hotels", "filters": {{"city": "New York"}}}}
Observation: I found 5 hotel(s) in New York:

1. **Grand Plaza Hotel** - $150/night
   ⭐ 4.5 stars | 4-star hotel
   ...

Final Answer: I found 5 hotel(s) in New York:

1. **Grand Plaza Hotel** - $150/night
   ⭐ 4.5 stars | 4-star hotel
   📍 123 Main Street
   ✨ WiFi, Pool, Gym
   🛏️ 5 rooms available

2. **Comfort Inn & Suites** - $95/night
   ...

Would you like to book one of these?

Example 2 - Direct booking:
User: "Book a hotel in NYC"
Thought: User wants to book. Need to collect info. Start with number of people.
Final Answer: I'll help you book a hotel in NYC. How many people will be staying?

Example 3 - User mentions specific place:
User: "I want to book the Grand Plaza Hotel"
Thought: User mentioned specific hotel. Show it with DisplayResults first.
Action: DisplayResults
Action Input: {{"type": "hotels", "filters": {{"city": "New York"}}}}
Observation: I found 5 hotel(s) in New York:

1. **Grand Plaza Hotel** - $150/night
   ⭐ 4.5 stars | 4-star hotel
   ...

Final Answer: Great choice! Here are hotels in the area including the Grand Plaza Hotel:

1. **Grand Plaza Hotel** - $150/night
   ⭐ 4.5 stars | 4-star hotel
   📍 123 Main Street
   
To book the Grand Plaza Hotel, how many people will be staying?

Example 4 - Collecting info (NO ACTION NEEDED):
User: "2 people"
Thought: Got people=2. Need check-in date next. Just ask directly, no tool needed.
Final Answer: Perfect! What is your check-in date? (Format: YYYY-MM-DD)

User: "2026-02-15"
Thought: Got checkin date. Need checkout date next. Just ask directly, no tool needed.
Final Answer: Great! What is your check-out date? (Format: YYYY-MM-DD)

User: "2026-02-18"  
Thought: Got checkout date. Need name now. Just ask directly, no tool needed.
Final Answer: Excellent! What name should the reservation be under?

Example 4b - User asks to see options mid-conversation:
User: "I need to make a restaurant reservation"
Final Answer: I'll help you book a restaurant. What city?

User: "New York"
Final Answer: How many people will be dining?

User: "4 people"
Final Answer: What date? (Format: YYYY-MM-DD)

User: "2026-01-08"
Final Answer: What time would you like?

User: "show me available times"
Thought: User wants to see restaurant options and their available times. Use DisplayResults.
Action: DisplayResults
Action Input: {{"type": "restaurants", "filters": {{"city": "New York"}}}}
Observation: I found 5 restaurant(s) in New York:

1. **The Italian Corner** - Italian
   ⭐ 4.7 stars | $$
   🕒 Available: 5:30 PM, 7:00 PM, 8:30 PM
...

Final Answer: Here are available restaurants in New York with their times:

1. **The Italian Corner** - Italian
   ⭐ 4.7 stars | $$
   🕒 Available: 5:30 PM, 7:00 PM, 8:30 PM

2. **Sakura Sushi Bar** - Japanese
   ⭐ 4.8 stars | $$$
   🕒 Available: 6:00 PM, 7:30 PM, 9:00 PM

Which restaurant and time would you prefer?

Example 5 - Final confirmation (USE TOOL):
User: "John Smith"
Thought: Have all info: city=NYC, people=2, checkin=2026-02-15, checkout=2026-02-18, name=John Smith. Time to confirm with ConfirmReservation tool.
Action: ConfirmReservation
Action Input: {{"type": "hotel", "city": "NYC", "people": "2", "checkin": "2026-02-15", "checkout": "2026-02-18", "name": "John Smith"}}
Observation: ✅ Hotel Reservation Confirmed! Confirmation: HOT-123456...
Final Answer: ✅ Your hotel reservation is confirmed! Confirmation number: HOT-123456. You'll receive an email confirmation shortly.

CRITICAL - WHEN TO USE ACTIONS VS FINAL ANSWER:
✅ Use Action + Tool when:
  - User asks to "show/find/search" → Use DisplayResults
  - You have ALL info collected → Use ConfirmReservation

❌ NO Action when:
  - Asking user a question → Use ONLY "Final Answer:"
  - Collecting information → Use ONLY "Final Answer:"
  - Responding without tools → Use ONLY "Final Answer:"

NEVER WRITE: "Action: None" - This is invalid! If you don't need a tool, skip Action entirely and go straight to Final Answer.

RULES:
- Use DisplayResults whenever user asks to "show", "find", "search", "see", or "display" options
- Use DisplayResults when user mentions a specific place name
- Use DisplayResults if user asks for "available times", "available hotels", "options", etc. - even mid-conversation
- Ask questions ONE AT A TIME
- Don't use tools between questions - just ask with Final Answer
- Only use ConfirmReservation when you have ALL required info
- If mid-conversation user wants to see options, show them with DisplayResults, then continue collecting info

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