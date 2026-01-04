"""
Shared tools for displaying data to the frontend
"""
from typing import Dict, Any, List
import json


class DataDisplayTool:
    """Tool for sending structured data to frontend while responding in chat"""
    
    # In-memory storage for the latest data to display
    # In production, this could be Redis, database, or session storage
    _display_data = {}
    
    @staticmethod
    def set_display_data(session_id: str, data_type: str, data: List[Dict[str, Any]]) -> None:
        """
        Store data to be sent to frontend
        
        Args:
            session_id: User session identifier
            data_type: Type of data (hotels, restaurants, flights)
            data: List of items to display
        """
        if session_id not in DataDisplayTool._display_data:
            DataDisplayTool._display_data[session_id] = {}
        
        DataDisplayTool._display_data[session_id] = {
            "type": data_type,
            "data": data,
            "timestamp": json.dumps({"timestamp": "now"})  # In production, use actual timestamp
        }
    
    @staticmethod
    def get_display_data(session_id: str) -> Dict[str, Any]:
        """
        Retrieve data for frontend display
        
        Args:
            session_id: User session identifier
            
        Returns:
            Dictionary with type and data to display
        """
        return DataDisplayTool._display_data.get(session_id, {})
    
    @staticmethod
    def clear_display_data(session_id: str) -> None:
        """Clear display data for a session"""
        if session_id in DataDisplayTool._display_data:
            del DataDisplayTool._display_data[session_id]
    
    @staticmethod
    def create_display_tool(session_id: str = "default"):
        """
        Create a tool function for displaying hotels/restaurants
        
        Args:
            session_id: Session identifier for storing data
            
        Returns:
            Function that can be used as a LangChain tool
        """
        from langchain_core.tools import Tool
        
        def display_results(query_json: str) -> str:
            """
            Display hotels, restaurants, or flights to the user.
            Also sends data to frontend for visual display.
            
            Input should be JSON with:
            - type: "hotels", "restaurants", or "flights"
            - filters: dict with search criteria
            
            Example: '{"type": "hotels", "filters": {"city": "New York", "max_price": 150}}'
            """
            try:
                query = json.loads(query_json)
                data_type = query.get("type", "").lower()
                filters = query.get("filters", {})
                
                # Generate dummy data based on type
                if data_type == "hotels":
                    data = generate_hotel_data(filters)
                elif data_type == "restaurants":
                    data = generate_restaurant_data(filters)
                elif data_type == "flights":
                    data = generate_flight_data(filters)
                else:
                    return "Invalid type. Use 'hotels', 'restaurants', or 'flights'"
                
                # Store data for frontend
                DataDisplayTool.set_display_data(session_id, data_type, data)
                
                # Create chat response
                response = create_chat_response(data_type, data, filters)
                
                # Return the chat response directly so agent can use it
                return response
                
            except Exception as e:
                return f"Error displaying results: {str(e)}"
        
        return Tool(
            name="DisplayResults",
            func=display_results,
            description="""Display hotels, restaurants, or flights to the user with visual cards in the frontend.
            Use this when user asks to 'show', 'display', 'find', or 'search for' hotels/restaurants/flights.
            Input must be JSON with type (hotels/restaurants/flights) and filters (search criteria).
            
            FILTER EXAMPLES:
            - Hotels: {{"type": "hotels", "filters": {{"city": "New York", "max_price": 150}}}}
            - Restaurants (cheap): {{"type": "restaurants", "filters": {{"city": "New York", "max_price_range": 1}}}}
            - Restaurants (moderate): {{"type": "restaurants", "filters": {{"city": "New York", "max_price_range": 2}}}}
            - Restaurants (expensive): {{"type": "restaurants", "filters": {{"city": "New York", "max_price_range": 3}}}}
            - Restaurants (luxury): {{"type": "restaurants", "filters": {{"city": "New York", "max_price_range": 4}}}}
            - Restaurants by cuisine: {{"type": "restaurants", "filters": {{"city": "New York", "cuisine": "Italian"}}}}
            - Flights: {{"type": "flights", "filters": {{"from": "Boston", "to": "New York", "max_price": 300}}}}
            
            PRICE RANGE for restaurants: 1=cheap($), 2=moderate($$), 3=expensive($$$), 4=luxury($$$$)"""
        )


def generate_hotel_data(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate dummy hotel data based on filters"""
    city = filters.get("city", "New York")
    max_price = filters.get("max_price", 500)
    min_rating = filters.get("min_rating", 0)
    
    all_hotels = [
        {
            "id": "hotel_1",
            "name": "Grand Plaza Hotel",
            "city": city,
            "address": "123 Main Street",
            "price_per_night": 150,
            "rating": 4.5,
            "stars": 4,
            "amenities": ["WiFi", "Pool", "Gym", "Restaurant", "Spa"],
            "image_url": "https://example.com/hotel1.jpg",
            "available_rooms": 5,
            "description": "Luxury hotel in the heart of downtown",
            "latitude": 41.7589,
            "latitude": -73.9851
        },
        {
            "id": "hotel_2",
            "name": "Comfort Inn & Suites",
            "city": city,
            "address": "456 Oak Avenue",
            "price_per_night": 95,
            "rating": 4.0,
            "stars": 3,
            "amenities": ["WiFi", "Parking", "Breakfast", "Gym"],
            "image_url": "https://example.com/hotel2.jpg",
            "available_rooms": 12,
            "description": "Comfortable and affordable accommodations",
            "latitude": 42.7589,
            "longitude": -73.9851
        },
        {
            "id": "hotel_3",
            "name": "Luxury Resort & Casino",
            "city": city,
            "address": "789 Beach Boulevard",
            "price_per_night": 275,
            "rating": 4.8,
            "stars": 5,
            "amenities": ["WiFi", "Pool", "Spa", "Casino", "Beach Access", "Fine Dining"],
            "image_url": "https://example.com/hotel3.jpg",
            "available_rooms": 3,
            "description": "5-star resort with world-class amenities",
            "latitude": 43.7589,
            "longitude": -73.9851
        },
        {
            "id": "hotel_4",
            "name": "Budget Lodge",
            "city": city,
            "address": "321 Highway 1",
            "price_per_night": 65,
            "rating": 3.5,
            "stars": 2,
            "amenities": ["WiFi", "Parking"],
            "image_url": "https://example.com/hotel4.jpg",
            "available_rooms": 20,
            "description": "Clean and simple budget accommodations",
            "latitude": 44.7589,
            "longitude": -73.9851
        },
        {
            "id": "hotel_5",
            "name": "Business Executive Hotel",
            "city": city,
            "address": "555 Corporate Drive",
            "price_per_night": 135,
            "rating": 4.3,
            "stars": 4,
            "amenities": ["WiFi", "Business Center", "Meeting Rooms", "Gym"],
            "image_url": "https://example.com/hotel5.jpg",
            "available_rooms": 8,
            "description": "Perfect for business travelers",
            "latitude": 45.7589,
            "longitude": -73.9851
        }
    ]
    
    # Apply filters
    filtered = [
        h for h in all_hotels 
        if h["price_per_night"] <= max_price and h["rating"] >= min_rating
    ]
    
    return filtered


def generate_restaurant_data(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate dummy restaurant data based on filters"""
    city = filters.get("city", "New York")
    cuisine = filters.get("cuisine", None)
    max_price_range = filters.get("max_price_range", 4)  # 1-4 scale
    
    # Handle different price filter formats
    if isinstance(max_price_range, str):
        # Convert "$" to 1, "$$" to 2, etc.
        max_price_range = len(max_price_range) if max_price_range.startswith("$") else 4
    
    all_restaurants = [
        {
            "id": "rest_1",
            "name": "The Italian Corner",
            "city": city,
            "address": "100 Pasta Lane",
            "cuisine": "Italian",
            "price_range": 2,
            "rating": 4.7,
            "phone": "(555) 123-4567",
            "image_url": "https://example.com/restaurant1.jpg",
            "available_times": ["5:30 PM", "7:00 PM", "8:30 PM"],
            "specialties": ["Handmade Pasta", "Wood-fired Pizza", "Tiramisu"],
            "latitude": 40.7589,
            "longitude": -73.9851
        },
        {
            "id": "rest_2",
            "name": "Sakura Sushi Bar",
            "city": city,
            "address": "200 Bamboo Street",
            "cuisine": "Japanese",
            "price_range": 3,
            "rating": 4.8,
            "phone": "(555) 234-5678",
            "image_url": "https://example.com/restaurant2.jpg",
            "available_times": ["6:00 PM", "7:30 PM", "9:00 PM"],
            "specialties": ["Omakase", "Sashimi", "Sake Selection"],
            "latitude": 40.7589,
            "longitude": -74.9851
        },
        {
            "id": "rest_3",
            "name": "Burger Palace",
            "city": city,
            "address": "300 Grill Avenue",
            "cuisine": "American",
            "price_range": 1,
            "rating": 4.2,
            "phone": "(555) 345-6789",
            "image_url": "https://example.com/restaurant3.jpg",
            "available_times": ["5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM"],
            "specialties": ["Signature Burger", "Craft Beer", "Milkshakes"],
            "latitude": 40.7589,
            "longitude": -75.9851
        },
        {
            "id": "rest_4",
            "name": "Le Petit Bistro",
            "city": city,
            "address": "400 Croissant Circle",
            "cuisine": "French",
            "price_range": 4,
            "rating": 4.9,
            "phone": "(555) 456-7890",
            "image_url": "https://example.com/restaurant4.jpg",
            "available_times": ["7:00 PM", "8:30 PM"],
            "specialties": ["Coq au Vin", "Crème Brûlée", "Wine Pairing"],
            "latitude": 40.7589,
            "longitude": -76.9851
        },
        {
            "id": "rest_5",
            "name": "Spice Garden",
            "city": city,
            "address": "500 Curry Court",
            "cuisine": "Indian",
            "price_range": 2,
            "rating": 4.6,
            "phone": "(555) 567-8901",
            "image_url": "https://example.com/restaurant5.jpg",
            "available_times": ["6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM"],
            "specialties": ["Butter Chicken", "Biryani", "Naan Bread"],
            "latitude": 40.7589,
            "longitude": -77.9851
        }
    ]
    
    # Apply filters
    filtered = all_restaurants
    if cuisine:
        filtered = [r for r in filtered if r["cuisine"].lower() == cuisine.lower()]
    if max_price_range:
        filtered = [r for r in filtered if r["price_range"] <= max_price_range]
    
    return filtered


def generate_flight_data(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate dummy flight data based on filters"""
    from_city = filters.get("from", "Boston")
    to_city = filters.get("to", "New York")
    max_price = filters.get("max_price", 1000)
    
    all_flights = [
        {
            "id": "flight_1",
            "airline": "SkyHigh Airlines",
            "flight_number": "SH123",
            "from": from_city,
            "to": to_city,
            "departure_time": "10:30 AM",
            "arrival_time": "2:45 PM",
            "duration": "4h 15m",
            "price": 350,
            "class": "Economy",
            "stops": 0,
            "aircraft": "Boeing 737",
            "available_seats": 45
        },
        {
            "id": "flight_2",
            "airline": "Budget Air",
            "flight_number": "BA456",
            "from": from_city,
            "to": to_city,
            "departure_time": "2:15 PM",
            "arrival_time": "7:30 PM",
            "duration": "5h 15m",
            "price": 215,
            "class": "Economy",
            "stops": 1,
            "aircraft": "Airbus A320",
            "available_seats": 78
        },
        {
            "id": "flight_3",
            "airline": "Premium Airways",
            "flight_number": "PA789",
            "from": from_city,
            "to": to_city,
            "departure_time": "8:00 AM",
            "arrival_time": "12:30 PM",
            "duration": "4h 30m",
            "price": 550,
            "class": "Business",
            "stops": 0,
            "aircraft": "Boeing 787",
            "available_seats": 12
        }
    ]
    
    # Apply filters
    filtered = [f for f in all_flights if f["price"] <= max_price]
    
    return filtered


def create_chat_response(data_type: str, data: List[Dict[str, Any]], filters: Dict[str, Any]) -> str:
    """Create a natural language chat response"""
    count = len(data)
    
    if count == 0:
        return f"I couldn't find any {data_type} matching your criteria. Try adjusting your filters."
    
    # Create summary
    if data_type == "hotels":
        city = filters.get("city", "the area")
        max_price = filters.get("max_price", "any price")
        response = f"I found {count} hotel(s) in {city}"
        if max_price != "any price":
            response += f" under ${max_price} per night"
        response += ":\n\n"
        
        # List all hotels
        for i, hotel in enumerate(data, 1):
            response += f"{i}. **{hotel['name']}** - ${hotel['price_per_night']}/night\n"
            response += f"   ⭐ {hotel['rating']} stars | {hotel['stars']}-star hotel\n"
            response += f"   🛏️ {hotel['available_rooms']} rooms available\n\n"
    
    elif data_type == "restaurants":
        city = filters.get("city", "the area")
        cuisine = filters.get("cuisine", "")
        response = f"I found {count} restaurant(s)"
        if cuisine:
            response += f" serving {cuisine} cuisine"
        response += f" in {city}:\n\n"
        
        # List all restaurants
        for i, rest in enumerate(data, 1):
            price_symbols = "$" * rest['price_range']
            response += f"{i}. **{rest['name']}** - {rest['cuisine']}\n"
            response += f"   🕒 Available: {', '.join(rest['available_times'][:3])}\n\n"
    
    elif data_type == "flights":
        from_city = filters.get("from", "your departure city")
        to_city = filters.get("to", "your destination")
        response = f"I found {count} flight(s) from {from_city} to {to_city}:\n\n"
        
        # List all flights
        for i, flight in enumerate(data, 1):
            stops_text = "Nonstop" if flight['stops'] == 0 else f"{flight['stops']} stop(s)"
            response += f"{i}. **{flight['airline']}** {flight['flight_number']} - ${flight['price']}\n"
            response += f"   🛫 Departs: {flight['departure_time']} → Arrives: {flight['arrival_time']}\n"
            response += f"   ⏱️ Duration: {flight['duration']} | {stops_text}\n"
            response += f"   💺 {flight['class']} | {flight['available_seats']} seats available\n\n"
    
    return response.strip()