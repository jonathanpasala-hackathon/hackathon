from agents.base_agent import BaseAgent
from agents.reservation_agent import EnhancedReservationAgent
from langchain_core.tools import Tool
from typing import List, Dict, Any
import json


class TripBookingAgent(BaseAgent):
    """Trip Booking Agent for coordinating multiple reservations"""
    
    def __init__(self):
        # Initialize a reservation agent instance to use as a tool
        self.reservation_agent = EnhancedReservationAgent()
        self.trip_state = {
            "reservations": [],  # List of completed reservations
            "current_step": None,  # What we're currently booking
            "pending_items": []  # Items still to book
        }
        super().__init__()
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for trip booking"""
        
        def plan_trip(details: str) -> str:
            """
            Analyze trip request and create a booking plan.
            Input: User's trip description
            Output: JSON with list of required reservations
            """
            try:
                # Parse what needs to be booked
                items = []
                details_lower = details.lower()
                
                # Check for explicit mentions
                has_flight = any(word in details_lower for word in ['flight', 'fly', 'plane', 'air'])
                has_hotel = any(word in details_lower for word in ['hotel', 'stay', 'accommodation', 'room'])
                has_restaurant = any(word in details_lower for word in ['restaurant', 'dining', 'dinner', 'lunch', 'eat'])
                
                # Implicit trip planning - if they say "trip" or "vacation" without specifics, assume flight + hotel
                is_general_trip = any(word in details_lower for word in ['trip', 'vacation', 'visit', 'travel to', 'going to', 'plan'])
                has_duration = any(word in details_lower for word in ['day', 'days', 'week', 'weeks', 'night', 'nights'])
                has_destination = not has_flight and not has_hotel and not has_restaurant  # They mentioned a destination but no specific bookings
                
                # If it's a general trip request with duration, assume they need flight + hotel
                if is_general_trip and (has_duration or has_destination) and not has_flight and not has_hotel:
                    has_flight = True
                    has_hotel = True
                
                # Add flight if needed
                if has_flight:
                    items.append({"type": "flight", "status": "pending"})
                
                # Add hotel if needed
                if has_hotel:
                    items.append({"type": "hotel", "status": "pending"})
                
                # Check for restaurant mentions or if it's a multi-day trip
                restaurant_keywords = ['restaurant', 'dining', 'dinner', 'lunch', 'eat']
                restaurant_count = sum(1 for word in restaurant_keywords if word in details_lower)
                
                # Check for multiple restaurant bookings
                if 'restaurants' in details_lower or restaurant_count > 1:
                    # Try to determine how many
                    import re
                    numbers = re.findall(r'\b(\d+)\s+restaurant', details_lower)
                    count = int(numbers[0]) if numbers else 2
                    for i in range(count):
                        items.append({"type": "restaurant", "number": i+1, "status": "pending"})
                elif has_restaurant:
                    items.append({"type": "restaurant", "status": "pending"})
                
                # If still no items detected but they're clearly planning a trip, ask for clarification
                if not items and is_general_trip:
                    return json.dumps({
                        "total_items": 0,
                        "items": [],
                        "message": "Need clarification: What would you like to book for this trip? (flight, hotel, restaurant, or all?)",
                        "needs_clarification": True
                    }, indent=2)
                
                self.trip_state["pending_items"] = items
                
                return json.dumps({
                    "total_items": len(items),
                    "items": items,
                    "message": f"Trip plan created: {len(items)} reservation(s) needed"
                }, indent=2)
                
            except Exception as e:
                return f"Error planning trip: {str(e)}"
        
        def start_reservation(reservation_type: str) -> str:
            """
            Start collecting info for a specific reservation type.
            Returns the list of questions to ask.
            """
            try:
                questions = {
                    "flight": [
                        "How many tickets do you need?",
                        "What city will you be departing from?",
                        "What city will you be flying to?",
                        "What is your departure date? (Format: YYYY-MM-DD)",
                        "Is this a round trip?",
                        "What is your return date? (if round trip, Format: YYYY-MM-DD)",
                        "What name should the reservation be under?"
                    ],
                    "hotel": [
                        "What city will you be staying in?",
                        "How many people will be staying?",
                        "What is your check-in date? (Format: YYYY-MM-DD)",
                        "What is your check-out date? (Format: YYYY-MM-DD)",
                        "What name should the reservation be under?"
                    ],
                    "restaurant": [
                        "What city is the restaurant in?",
                        "How many people will be dining?",
                        "What date would you like to dine? (Format: YYYY-MM-DD)",
                        "What time would you prefer?",
                        "What name should the reservation be under?"
                    ]
                }
                
                return json.dumps({
                    "reservation_type": reservation_type,
                    "questions": questions.get(reservation_type, []),
                    "first_question": questions.get(reservation_type, [""])[0]
                }, indent=2)
                
            except Exception as e:
                return f"Error starting reservation: {str(e)}"
        
        def complete_reservation(confirmation_details: str) -> str:
            """
            Mark current reservation as complete.
            """
            try:
                # Mark as completed
                if self.trip_state["pending_items"]:
                    for item in self.trip_state["pending_items"]:
                        if item["status"] == "pending":
                            item["status"] = "completed"
                            item["confirmation"] = confirmation_details
                            self.trip_state["reservations"].append(item)
                            break
                
                # Check remaining
                pending_count = sum(1 for item in self.trip_state["pending_items"] 
                                   if item["status"] == "pending")
                
                return json.dumps({
                    "status": "completed",
                    "total_completed": len(self.trip_state["reservations"]),
                    "remaining": pending_count,
                    "all_done": pending_count == 0
                }, indent=2)
                
            except Exception as e:
                return f"Error completing reservation: {str(e)}"
        
        def get_trip_summary() -> str:
            """Get summary of all reservations in the trip."""
            try:
                summary = {
                    "total_reservations": len(self.trip_state["reservations"]),
                    "completed": [],
                    "pending": []
                }
                
                for res in self.trip_state["reservations"]:
                    summary["completed"].append({
                        "type": res["type"],
                        "confirmation": res.get("confirmation", "N/A")
                    })
                
                for item in self.trip_state["pending_items"]:
                    if item["status"] == "pending":
                        summary["pending"].append(item["type"])
                
                return json.dumps(summary, indent=2)
                
            except Exception as e:
                return f"Error getting summary: {str(e)}"
        
        return [
            Tool(
                name="PlanTrip",
                func=plan_trip,
                description="Analyze the user's trip request and create a plan of what needs to be booked (flights, hotels, restaurants). Use this ONCE at the start."
            ),
            Tool(
                name="StartReservation",
                func=start_reservation,
                description="Start a new reservation (flight, hotel, or restaurant). Input: reservation type. Returns list of questions to ask. Use this when starting each new reservation type."
            ),
            Tool(
                name="CompleteReservation",
                func=complete_reservation,
                description="Mark the current reservation as complete after collecting ALL required info including name. Input: summary of collected information."
            ),
            Tool(
                name="GetTripSummary",
                func=get_trip_summary,
                description="Get a summary of all completed and pending reservations in this trip. Use at the end to show final itinerary."
            )
        ]
    
    def get_prompt_template(self) -> str:
        return """You are a trip booking assistant that helps users book complete trips with multiple reservations (flights, hotels, restaurants).

WORKFLOW:
1. User describes trip → Use PlanTrip ONCE
2. Use StartReservation with the first type (flight/hotel/restaurant)
3. Ask questions ONE AT A TIME - just use Final Answer (no Action needed)
4. Track answers in your memory - the conversation history shows all responses
5. When you have ALL required info + name → Use CompleteReservation
6. Use StartReservation for the next type
7. Repeat until all done
8. Use GetTripSummary to show final itinerary

REQUIRED INFO (ask in order):

FLIGHT:
1. Number of tickets
2. Departing city
3. Arriving city (often mentioned in original request)
4. Departure date (YYYY-MM-DD)
5. Round trip? (yes/no)
6. Return date if round trip (YYYY-MM-DD)
7. Name on reservation ← MUST GET THIS

HOTEL:
1. City (often same as flight destination)
2. Number of people
3. Check-in date (YYYY-MM-DD)
4. Check-out date (YYYY-MM-DD)
5. Name on reservation ← MUST GET THIS

RESTAURANT:
1. City
2. Number of people
3. Date (YYYY-MM-DD)
4. Time
5. Name on reservation ← MUST GET THIS

EXAMPLE:

User: "Plan a trip to NYC for 3 days"

Thought: Need to create trip plan.
Action: PlanTrip
Action Input: Plan a trip to NYC for 3 days
Observation: {{"total_items": 2, "items": [{{"type": "flight"}}, {{"type": "hotel"}}]}}
Thought: Plan created. Start with flight.
Action: StartReservation
Action Input: flight
Observation: {{"first_question": "How many tickets do you need?"}}
Thought: Ready to ask first flight question.
Final Answer: Great! I'll help plan your 3-day NYC trip. Let's start with your flight. How many tickets do you need?

User: "2"
Thought: Got tickets=2. Need departing city next.
Final Answer: Perfect! What city will you be departing from?

User: "Boston"
Thought: Got tickets=2, departing=Boston. Destination is NYC from original request. Need departure date.
Final Answer: What is your departure date? (Format: YYYY-MM-DD)

User: "2026-02-15"
Thought: Got tickets=2, departing=Boston, arriving=NYC, departure=2026-02-15. Need to know if round trip.
Final Answer: Is this a round trip?

User: "Yes"
Thought: Round trip. Need return date.
Final Answer: When would you like to return? (Format: YYYY-MM-DD)

User: "2026-02-18"
Thought: Got tickets=2, departing=Boston, arriving=NYC, depart 2/15, return 2/18. Need name for reservation.
Final Answer: What name should the flight reservation be under?

User: "Sarah Johnson"
Thought: Have ALL flight info: tickets=2, departing=Boston, arriving=NYC, depart 2/15, return 2/18, name=Sarah Johnson. Complete it.
Action: CompleteReservation
Action Input: Flight confirmed - 2 tickets, Boston to NYC, depart 2/15/2026, return 2/18/2026, name Sarah Johnson
Observation: {{"remaining": 1, "all_done": false}}
Thought: Flight complete. Start hotel booking.
Action: StartReservation
Action Input: hotel
Observation: {{"first_question": "What city will you be staying in?"}}
Thought: Ready to ask first hotel question.
Final Answer: Excellent! Your flight is booked. Now for your hotel in NYC. How many people will be staying?

You have access to these tools:
{tools}

Tool names: {tool_names}

Use the following format:

Question: {input}
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