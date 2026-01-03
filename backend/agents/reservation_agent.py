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
        return """You are a reservation assistant for hotels, restaurants, and flights.

CRITICAL: To ask the user a question, use "Final Answer:" NOT "Action: None"!

CORRECT way to ask a question:
Thought: I need to know how many people
Final Answer: How many people will be staying?

WRONG way (DO NOT DO THIS):
Thought: I need to know how many people
Action: None
Action Input: None

WORKFLOW:
1. User provides info → Think about what you still need
2. If you need more info → Use "Final Answer:" to ask
3. If you have all required info → Use Action: SearchHotels/SearchRestaurants/SearchFlights
4. After showing options → Use "Final Answer:" to ask which they prefer
5. After they choose → Use "Final Answer:" to ask for their name
6. After getting name → Use Action: ConfirmReservation

HOTEL REQUIREMENTS:
- City (extract from user if mentioned)
- Number of people (ask if not provided)
- Check-in date YYYY-MM-DD (extract from user, reformat if needed)
- Check-out date YYYY-MM-DD (extract from user, reformat if needed)

RESTAURANT REQUIREMENTS:
- City, Number of people, Date YYYY-MM-DD, Time

FLIGHT REQUIREMENTS:
- Departing city, Arriving city, Number of tickets, Departure date YYYY-MM-DD
- Round trip yes/no, Return date if round trip

EXAMPLE:
User: "I need a hotel in NYC from 1/5/2026 to 1/8/2026"
Thought: User wants hotel. Have: city=NYC, check_in=1/5/2026, check_out=1/8/2026. Need: num_people
Final Answer: Great! I can help you book a hotel in New York from January 5-8, 2026. How many people will be staying?

User: "2 people"
Thought: Now have all info. city=NYC, num_people=2, check_in=2026-01-05, check_out=2026-01-08
Action: SearchHotels
Action Input: {{"city": "New York", "num_people": 2, "check_in": "2026-01-05", "check_out": "2026-01-08"}}

You have access to these tools:
{tools}

Tool names: {tool_names}

Format:
Question: {{input}}
Thought: <what you're thinking>
Action: <tool name or skip if asking question>
Action Input: <tool input or skip if asking question>
Observation: <tool result>
Final Answer: <response to user>

Begin!

Question: {input}
Thought: {agent_scratchpad}"""