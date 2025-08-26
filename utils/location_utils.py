"""
Location utilities for the ride app
"""

import webbrowser
import urllib.parse

class LocationUtils:
    @staticmethod
    def open_google_maps(pickup_location, drop_location):
        """Open Google Maps with directions from pickup to drop location"""
        try:
            # Encode locations for URL
            pickup_encoded = urllib.parse.quote(pickup_location)
            drop_encoded = urllib.parse.quote(drop_location)
            
            # Create Google Maps directions URL
            maps_url = f"https://www.google.com/maps/dir/{pickup_encoded}/{drop_encoded}"
            
            # Open in default browser
            webbrowser.open(maps_url)
            return True
        except Exception as e:
            print(f"Error opening Google Maps: {e}")
            return False
    
    @staticmethod
    def get_sample_locations():
        """Get sample locations for testing"""
        return [
            "Central Park, New York",
            "Times Square, New York",
            "Empire State Building, New York",
            "Brooklyn Bridge, New York",
            "Statue of Liberty, New York",
            "Central Station, New York",
            "Madison Square Garden, New York",
            "Rockefeller Center, New York"
        ]
    
    @staticmethod
    def validate_location(location):
        """Basic location validation"""
        if not location or len(location.strip()) < 3:
            return False
        return True
    
    @staticmethod
    def format_location(location):
        """Format location for display"""
        return location.strip().title()
    
    @staticmethod
    def get_distance_estimate(pickup, drop):
        """Get rough distance estimate (simplified)"""
        # This is a very simplified distance calculation
        # In a real app, you'd use actual geocoding and distance APIs
        
        # Simple character-based "distance" for demo purposes
        pickup_len = len(pickup)
        drop_len = len(drop)
        
        # Simulate distance based on string length difference
        base_distance = abs(pickup_len - drop_len) * 0.5 + 2.0
        
        # Add some randomness
        import random
        random_factor = random.uniform(0.8, 1.2)
        
        return round(base_distance * random_factor, 1)
    
    @staticmethod
    def get_estimated_fare(pickup, drop):
        """Get estimated fare based on distance"""
        distance = LocationUtils.get_distance_estimate(pickup, drop)
        base_fare = 5.0
        per_mile_rate = 2.5
        
        estimated_fare = base_fare + (distance * per_mile_rate)
        return round(estimated_fare, 2)
