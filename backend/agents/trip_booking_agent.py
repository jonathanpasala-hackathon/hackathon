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
                
                if any(word in details_lower for word in ['flight', 'fly', 'plane']):
                    items.append({"type": "flight", "status": "pending"})
                
                if any(word in details_lower for word in ['hotel', 'stay', 'accommodation', 'room']):
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
                elif any(word in details_lower for word in restaurant_keywords):
                    items.append({"type": "restaurant", "status": "pending"})
                
                self.trip_state["pending_items"] = items
                
                return json.dumps({
                    "total_items": len(items),
                    "items": items,
                    "message": f"Trip plan created: {len(items)} reservation(s) needed"
                }, indent=2)
                
            except Exception as e:
                return f"Error planning trip: {str(e)}"
        
        def book_next_item(context: str = "") -> str: # type: ignore
            """
            Start booking the next pending item using the reservation agent.
            Returns the question the reservation agent would ask.
            """
            try:
                if not self.trip_state["pending_items"]:
                    return "All reservations completed!"
                
                # Get next item to book
                next_item = None
                for item in self.trip_state["pending_items"]:
                    if item["status"] == "pending":
                        next_item = item
                        break
                
                if not next_item:
                    return "All reservations completed!"
                
                # Mark as in progress
                next_item["status"] = "in_progress"
                self.trip_state["current_step"] = next_item
                
                # Determine what type of reservation to start
                res_type = next_item["type"]
                number = next_item.get("number", "")
                
                if res_type == "flight":
                    return json.dumps({
                        "reservation_type": "flight",
                        "message": "Let's book your flight. How many tickets do you need?",
                        "next_questions": ["departing city", "arriving city", "departure date", "round trip?"]
                    })
                elif res_type == "hotel":
                    return json.dumps({
                        "reservation_type": "hotel",
                        "message": "Let's book your hotel. What city will you be staying in?",
                        "next_questions": ["number of people", "check-in date", "check-out date"]
                    })
                elif res_type == "restaurant":
                    restaurant_label = f" #{number}" if number else ""
                    return json.dumps({
                        "reservation_type": "restaurant",
                        "message": f"Let's book restaurant{restaurant_label}. What city is the restaurant in?",
                        "next_questions": ["number of people", "date", "time"]
                    })
                
            except Exception as e:
                return f"Error starting next booking: {str(e)}"
        
        def collect_reservation_info(user_response: str) -> str:
            """
            Collect information for the current reservation being booked.
            This simulates interaction with the reservation agent.
            """
            try:
                current = self.trip_state.get("current_step")
                if not current:
                    return "No active reservation. Use book_next_item first."
                
                # Store the response (in a real implementation, this would feed to reservation agent)
                if "collected_info" not in current:
                    current["collected_info"] = []
                
                current["collected_info"].append(user_response)
                
                return json.dumps({
                    "status": "info_collected",
                    "current_type": current["type"],
                    "collected_count": len(current["collected_info"]),
                    "user_response": user_response
                })
                
            except Exception as e:
                return f"Error collecting info: {str(e)}"
        
        def complete_current_reservation(confirmation_details: str) -> str:
            """
            Mark current reservation as complete and add to completed list.
            """
            try:
                current = self.trip_state.get("current_step")
                if not current:
                    return "No active reservation to complete."
                
                # Mark as completed
                current["status"] = "completed"
                current["confirmation"] = confirmation_details
                
                # Move to completed reservations
                self.trip_state["reservations"].append(current)
                self.trip_state["current_step"] = None
                
                # Check if more items pending
                pending_count = sum(1 for item in self.trip_state["pending_items"] 
                                   if item["status"] == "pending")
                
                return json.dumps({
                    "status": "completed",
                    "completed_type": current["type"],
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
                description="Analyze the user's trip request and create a plan of what needs to be booked (flights, hotels, restaurants). Use this first when user describes their trip."
            ),
            Tool(
                name="BookNextItem",
                func=book_next_item,
                description="Start booking the next item in the trip plan. This will return what question to ask the user for that specific reservation type."
            ),
            Tool(
                name="CollectReservationInfo",
                func=collect_reservation_info,
                description="Collect user's response for the current reservation being booked. Use this to store each piece of information provided."
            ),
            Tool(
                name="CompleteCurrentReservation",
                func=complete_current_reservation,
                description="Mark the current reservation as complete after all information is collected and confirmed. Input should include confirmation details."
            ),
            Tool(
                name="GetTripSummary",
                func=get_trip_summary,
                description="Get a summary of all completed and pending reservations in this trip."
            )
        ]
    
    def get_prompt_template(self) -> str:
        return """You are a trip booking assistant that helps users book complete trips with multiple reservations (flights, hotels, restaurants).

Your job is to coordinate multiple bookings in sequence, collecting all necessary information for each one.

WORKFLOW:
1. User describes their trip needs
2. Use PlanTrip to analyze what needs to be booked
3. Use BookNextItem to start the first reservation
4. Ask the user the questions indicated for that reservation type
5. Use CollectReservationInfo to store each response
6. Once you have all info for current reservation, use CompleteCurrentReservation
7. Use BookNextItem to move to the next reservation
8. Repeat until all reservations complete
9. Use GetTripSummary to show final trip overview

IMPORTANT RULES:
- Handle ONE reservation at a time
- Ask ONE question at a time using Final Answer
- Don't move to next reservation until current one is complete
- Keep track of what's been booked and what's pending
- After each reservation completes, tell user what's next

RESERVATION REQUIREMENTS:

FLIGHT:
- Number of tickets
- Departing city
- Arriving city  
- Departure date (YYYY-MM-DD)
- Round trip? (yes/no)
- If yes: Return date
- Name on reservation

HOTEL:
- City
- Number of people
- Check-in date (YYYY-MM-DD)
- Check-out date (YYYY-MM-DD)
- Name on reservation

RESTAURANT:
- City
- Number of people
- Date (YYYY-MM-DD)
- Time
- Name on reservation

EXAMPLE FLOW:

User: "I need to book a trip to Paris - flight and hotel"

Thought: User wants multiple reservations. Need to plan the trip first.
Action: PlanTrip
Action Input: I need to book a trip to Paris - flight and hotel
Observation: {{"total_items": 2, "items": [{{"type": "flight"}}, {{"type": "hotel"}}]}}

Thought: Plan created. Start with first item (flight).
Action: BookNextItem
Observation: {{"reservation_type": "flight", "message": "Let's book your flight. How many tickets do you need?"}}

Thought: Need to ask about tickets.
Final Answer: Let's start by booking your flight to Paris! How many tickets do you need?

[User provides info, you collect it, complete that reservation, then move to hotel, etc.]

You have access to these tools:
{tools}

Tool names: {tool_names}

Format:
Question: {input}
Thought: <what you're thinking>
Action: <tool name>
Action Input: <tool input>
Observation: <tool result>
Final Answer: <response to user>

Begin!

Question: {input}
Thought: {agent_scratchpad}"""