from db.connection import db_connection
from models.ride import Ride
from datetime import datetime

class RideManager:
    def __init__(self):
        self.db = db_connection.get_database()
    
    def request_ride(self, rider_email, pickup_location, drop_location):
        """Request a new ride"""
        try:
            ride = Ride(rider_email, pickup_location, drop_location)
            self.db.rides.insert_one(ride.to_dict())
            return True, ride.ride_id, "Ride requested successfully"
        except Exception as e:
            return False, None, f"Failed to request ride: {str(e)}"
    
    def get_available_rides(self):
        """Get all available rides for drivers"""
        try:
            rides = list(self.db.rides.find({"status": "requested"}))
            print(f"DEBUG: Available rides fetched: {rides}")  # Debug log
            return [Ride.from_dict(ride) for ride in rides]
        except Exception as e:
            print(f"DEBUG: Error fetching available rides: {e}")  # Debug log
            return []
    
    def accept_ride(self, ride_id, driver_email):
        """Driver accepts a ride"""
        try:
            ride_data = self.db.rides.find_one({"ride_id": ride_id})
            if not ride_data:
                return False, "Ride not found"
            
            ride = Ride.from_dict(ride_data)
            if ride.accept_ride(driver_email):
                # Update database
                self.db.rides.update_one(
                    {"ride_id": ride_id},
                    {"$set": ride.to_dict()}
                )
                # Update driver availability
                self.db.users.update_one(
                    {"email": driver_email},
                    {"$set": {"is_available": False, "current_ride": ride_id}}
                )
                return True, "Ride accepted successfully"
            else:
                return False, "Ride cannot be accepted"
        except Exception as e:
            return False, f"Failed to accept ride: {str(e)}"
    
    def start_ride(self, ride_id, driver_email):
        """Driver starts the ride"""
        try:
            ride_data = self.db.rides.find_one({"ride_id": ride_id})
            if not ride_data:
                return False, "Ride not found"
            
            ride = Ride.from_dict(ride_data)
            if ride.start_ride():
                self.db.rides.update_one(
                    {"ride_id": ride_id},
                    {"$set": ride.to_dict()}
                )
                return True, "Ride started successfully"
            else:
                return False, "Ride cannot be started"
        except Exception as e:
            return False, f"Failed to start ride: {str(e)}"
    
    def complete_ride(self, ride_id, driver_email):
        """Driver completes the ride"""
        try:
            ride_data = self.db.rides.find_one({"ride_id": ride_id})
            if not ride_data:
                return False, "Ride not found"
            
            ride = Ride.from_dict(ride_data)
            if ride.complete_ride():
                # Update ride
                self.db.rides.update_one(
                    {"ride_id": ride_id},
                    {"$set": ride.to_dict()}
                )
                # Update driver availability
                self.db.users.update_one(
                    {"email": driver_email},
                    {"$set": {"is_available": True, "current_ride": None}}
                )
                # Update user ride counts
                self.db.users.update_one(
                    {"email": ride.rider_email},
                    {"$inc": {"total_rides": 1}}
                )
                self.db.users.update_one(
                    {"email": driver_email},
                    {"$inc": {"total_rides": 1}}
                )
                return True, "Ride completed successfully"
            else:
                return False, "Ride cannot be completed"
        except Exception as e:
            return False, f"Failed to complete ride: {str(e)}"
    
    def cancel_ride(self, ride_id, user_email):
        """Cancel a ride"""
        try:
            ride_data = self.db.rides.find_one({"ride_id": ride_id})
            if not ride_data:
                return False, "Ride not found"
            
            ride = Ride.from_dict(ride_data)
            if ride.cancel_ride():
                self.db.rides.update_one(
                    {"ride_id": ride_id},
                    {"$set": ride.to_dict()}
                )
                
                # If driver had accepted, make them available again
                if ride.driver_email:
                    self.db.users.update_one(
                        {"email": ride.driver_email},
                        {"$set": {"is_available": True, "current_ride": None}}
                    )
                
                return True, "Ride cancelled successfully"
            else:
                return False, "Ride cannot be cancelled"
        except Exception as e:
            return False, f"Failed to cancel ride: {str(e)}"
    
    def get_user_rides(self, user_email):
        """Get all rides for a user"""
        try:
            rides = list(self.db.rides.find({
                "$or": [
                    {"rider_email": user_email},
                    {"driver_email": user_email}
                ]
            }))
            print(f"DEBUG: User rides fetched for {user_email}: {rides}")  # Debug log
            return [Ride.from_dict(ride) for ride in rides]
        except Exception as e:
            print(f"DEBUG: Error fetching user rides for {user_email}: {e}")  # Debug log
            return []
    
    def rate_ride(self, ride_id, rating):
        """Rate a completed ride"""
        try:
            ride_data = self.db.rides.find_one({"ride_id": ride_id})
            if not ride_data:
                return False, "Ride not found"
            
            ride = Ride.from_dict(ride_data)
            if ride.status != "completed":
                return False, "Can only rate completed rides"
            
            if ride.add_rating(rating):
                self.db.rides.update_one(
                    {"ride_id": ride_id},
                    {"$set": ride.to_dict()}
                )
                return True, "Rating added successfully"
            else:
                return False, "Invalid rating"
        except Exception as e:
            return False, f"Failed to add rating: {str(e)}"
    
    def get_ride_by_id(self, ride_id):
        """Get ride by ID"""
        try:
            ride_data = self.db.rides.find_one({"ride_id": ride_id})
            if ride_data:
                return Ride.from_dict(ride_data)
            return None
        except Exception:
            return None
