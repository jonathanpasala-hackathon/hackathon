from agents.base_agent import BaseAgent
from langchain_core.tools import Tool
from typing import List, Dict, Any, Optional
import json
from datetime import datetime


class EnhancedReservationAgent(BaseAgent):
    """Enhanced Reservation Agent with detailed information collection"""
    
    def __init__(self):
        super().__init__()
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for making reservations"""
        
        def search_hotels(criteria_json: str) -> str:
            """Search for available hotels - placeholder"""
            try:
                criteria = json.loads(criteria_json)
                city = criteria.get('city', 'Unknown')
                # Placeholder hotel results
                hotels = [
                    {
                        "name": "Grand Hotel Plaza",
                        "price": "$150/night",
                        "area": criteria.get('area', 'Downtown'),
                        "rating": "4.5 stars",
                        "amenities": ["Pool", "WiFi", "Breakfast"]
                    },
                    {
                        "name": "Comfort Inn & Suites",
                        "price": "$95/night",
                        "area": criteria.get('area', 'Midtown'),
                        "rating": "4.0 stars",
                        "amenities": ["WiFi", "Parking", "Gym"]
                    },
                    {
                        "name": "Luxury Resort Hotel",
                        "price": "$275/night",
                        "area": criteria.get('area', 'Waterfront'),
                        "rating": "5.0 stars",
                        "amenities": ["Spa", "Pool", "Beach Access", "Restaurant"]
                    }
                ]
                return json.dumps(hotels, indent=2)
            except Exception as e:
                return f"Error searching hotels: {str(e)}"
        
        def search_restaurants(criteria_json: str) -> str:
            """Search for available restaurants - placeholder"""
            try:
                criteria = json.loads(criteria_json)
                restaurants = [
                    {
                        "name": "The Italian Corner",
                        "cuisine": "Italian",
                        "price_range": "$$",
                        "area": criteria.get('area', 'Downtown'),
                        "rating": "4.7 stars",
                        "available_times": ["6:00 PM", "7:30 PM", "9:00 PM"]
                    },
                    {
                        "name": "Sakura Sushi Bar",
                        "cuisine": "Japanese",
                        "price_range": "$$$",
                        "area": criteria.get('area', 'Midtown'),
                        "rating": "4.8 stars",
                        "available_times": ["5:30 PM", "7:00 PM", "8:30 PM"]
                    },
                    {
                        "name": "Burger Palace",
                        "cuisine": "American",
                        "price_range": "$",
                        "area": criteria.get('area', 'West End'),
                        "rating": "4.2 stars",
                        "available_times": ["6:00 PM", "7:00 PM", "8:00 PM"]
                    }
                ]
                return json.dumps(restaurants, indent=2)
            except Exception as e:
                return f"Error searching restaurants: {str(e)}"
        
        def search_flights(criteria_json: str) -> str:
            """Search for available flights - placeholder"""
            try:
                criteria = json.loads(criteria_json)
                flights = [
                    {
                        "airline": "SkyHigh Airlines",
                        "flight_number": "SH123",
                        "departure_time": "10:30 AM",
                        "arrival_time": "2:45 PM",
                        "price": "$350",
                        "class": "Economy",
                        "stops": "Non-stop"
                    },
                    {
                        "airline": "Budget Air",
                        "flight_number": "BA456",
                        "departure_time": "2:15 PM",
                        "arrival_time": "7:30 PM",
                        "price": "$215",
                        "class": "Economy",
                        "stops": "1 stop"
                    },
                    {
                        "airline": "Premium Airways",
                        "flight_number": "PA789",
                        "departure_time": "8:00 AM",
                        "arrival_time": "12:30 PM",
                        "price": "$550",
                        "class": "Business",
                        "stops": "Non-stop"
                    }
                ]
                return json.dumps(flights, indent=2)
            except Exception as e:
                return f"Error searching flights: {str(e)}"
        
        def confirm_reservation(details_json: str) -> str:
            """Confirm and finalize reservation - placeholder"""
            try:
                details = json.loads(details_json)
                
                # Check if name is provided
                if not details.get('reservation_name'):
                    return "ERROR: Name on reservation is required before confirming"
                
                reservation_type = details.get('type', 'unknown')
                name = details.get('reservation_name')
                
                # Generate confirmation number
                import random
                conf_number = f"{reservation_type[:3].upper()}-{random.randint(100000, 999999)}"
                
                confirmation = {
                    "status": "CONFIRMED",
                    "confirmation_number": conf_number,
                    "reservation_name": name,
                    "type": reservation_type,
                    "details": details,
                    "timestamp": datetime.now().isoformat()
                }
                
                return json.dumps(confirmation, indent=2)
            except Exception as e:
                return f"Error confirming reservation: {str(e)}"
        
        return [
            Tool(
                name="SearchHotels",
                func=search_hotels,
                description="Search for available hotels based on criteria. "
                           "Input must be JSON string with: city, check_in, check_out, num_people. "
                           "Optional: area, price_range. "
                           "Example: '{\"city\": \"Paris\", \"check_in\": \"2024-06-15\", \"check_out\": \"2024-06-18\", \"num_people\": 2}'"
            ),
            Tool(
                name="SearchRestaurants",
                func=search_restaurants,
                description="Search for available restaurants based on criteria. "
                           "Input must be JSON string with: city, date, time, num_people. "
                           "Optional: area, price_range. "
                           "Example: '{\"city\": \"Chicago\", \"date\": \"2024-04-15\", \"time\": \"7:00 PM\", \"num_people\": 4}'"
            ),
            Tool(
                name="SearchFlights",
                func=search_flights,
                description="Search for available flights based on criteria. "
                           "Input must be JSON string with: departing_city, arriving_city, departure_date, num_tickets. "
                           "Optional: is_round_trip, return_date, price_range, airline_preference. "
                           "Example: '{\"departing_city\": \"LAX\", \"arriving_city\": \"NYC\", \"departure_date\": \"2024-07-20\", \"num_tickets\": 2}'"
            ),
            Tool(
                name="ConfirmReservation",
                func=confirm_reservation,
                description="Confirm and finalize the reservation. MUST include reservation_name. "
                           "Input must be complete JSON with all details including type, selected option, and reservation_name. "
                           "Example: '{\"type\": \"hotel\", \"city\": \"Paris\", \"selected\": \"Grand Hotel Plaza\", \"reservation_name\": \"John Smith\", ...}'"
            )
        ]
    
    def get_prompt_template(self) -> str:
        return """You are a reservation assistant that helps users book hotels, restaurants, and flights.

⚠️ CRITICAL RULES ⚠️
1. NEVER use SearchHotels/SearchRestaurants/SearchFlights on the first turn!
2. ALWAYS ask for required information FIRST using Final Answer
3. Tools are ONLY for searching AFTER you have all required info
4. One question at a time in your Final Answer

CORRECT START:
User: "I need a hotel in New York"
Thought: User wants hotel in New York. I need: num_people, check_in, check_out. Ask first question.
Final Answer: "I'd be happy to help you book a hotel in New York! How many people will be staying?"

WRONG START (DO NOT DO THIS):
User: "I need a hotel in New York"  
Action: SearchHotels  ← WRONG! Don't search yet!

REQUIRED INFORMATION BY TYPE:

HOTEL (need ALL before searching):
- City ✓ (get from user message if mentioned)
- Number of people (ASK)
- Check-in date in YYYY-MM-DD format (ASK)
- Check-out date in YYYY-MM-DD format (ASK)
Then → Use SearchHotels tool
Optional: Area, Price range
Must get: Selected hotel, Name on reservation

RESTAURANT (need ALL before searching):
- City ✓ (get from user message if mentioned)
- Number of people (ASK)
- Date in YYYY-MM-DD format (ASK)
- Time (ASK)
Then → Use SearchRestaurants tool
Optional: Area, Price range  
Must get: Selected restaurant, Name on reservation

FLIGHT (need ALL before searching):
- Number of tickets (ASK)
- Departing city ✓ (get from user message if mentioned)
- Arriving city (ASK if not mentioned)
- Departure date in YYYY-MM-DD format (ASK)
- Round trip? yes/no (ASK)
- If yes, return date (ASK)
Then → Use SearchFlights tool
Optional: Price range, Airline, Seats, Add-ons
Must get: Selected flight, Name on reservation

WORKFLOW STEPS:
1. Identify reservation type from user message
2. Extract any info already provided (like city)
3. Ask for MISSING required info ONE question at a time via Final Answer
4. When you have ALL required info → Use Search tool with JSON
5. Present options to user via Final Answer
6. User selects → Ask for name via Final Answer
7. User provides name → Use ConfirmReservation tool

EXAMPLE FULL FLOW:

Turn 1:
User: "I need a hotel in New York"
Thought: Hotel in New York. Have city="New York". Need: num_people, check_in, check_out
Final Answer: "I'd be happy to help you book a hotel in New York! How many people will be staying?"

Turn 2:
User: "2 people"
Thought: Have city="New York", num_people=2. Need: check_in, check_out
Final Answer: "Great! What is your check-in date? (Format: YYYY-MM-DD)"

Turn 3:
User: "2024-06-15"
Thought: Have city, people, check_in="2024-06-15". Need: check_out
Final Answer: "And when will you be checking out? (Format: YYYY-MM-DD)"

Turn 4:
User: "2024-06-18"
Thought: Have all required info! Search for hotels now.
Action: SearchHotels
Action Input: {{"city": "New York", "num_people": 2, "check_in": "2024-06-15", "check_out": "2024-06-18"}}
Observation: [{{"name": "Grand Hotel Plaza", "price": "$150/night", ...}}]
Thought: Got results. Show options to user.
Final Answer: "Here are available hotels:
1. Grand Hotel Plaza - $150/night, 4.5 stars
2. Comfort Inn - $95/night, 4.0 stars
Which would you prefer?"

Turn 5:
User: "Grand Hotel Plaza"
Thought: User selected. Need name before confirming.
Final Answer: "Excellent! What name should the reservation be under?"

Turn 6:
User: "John Smith"
Thought: Have everything. Confirm now.
Action: ConfirmReservation
Action Input: {{"type": "hotel", "city": "New York", "selected": "Grand Hotel Plaza", "reservation_name": "John Smith", "check_in": "2024-06-15", "check_out": "2024-06-18", "num_people": 2}}

You have access to the following tools:
{tools}

Tool names: {tool_names}

Use this format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""