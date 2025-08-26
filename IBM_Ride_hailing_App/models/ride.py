from datetime import datetime
import random

class Ride:
    def __init__(self, rider_email, pickup_location, drop_location):
        self.ride_id = self._generate_ride_id()
        self.rider_email = rider_email
        self.driver_email = None
        self.pickup_location = pickup_location
        self.drop_location = drop_location
        self.status = "requested"  # requested, accepted, started, completed, cancelled
        self.requested_at = datetime.now()
        self.accepted_at = None
        self.started_at = None
        self.completed_at = None
        self.fare = self._calculate_fare()
        self.rating = None
        self.payment_status = "pending"
    
    def _generate_ride_id(self):
        """Generate a unique ride ID"""
        return f"RIDE{random.randint(1000, 9999)}"
    
    def _calculate_fare(self):
        """Calculate fare based on distance (simplified)"""
        # Simple fare calculation - in real app would use actual distance
        base_fare = 10.0
        distance_multiplier = random.uniform(1.0, 3.0)
        return round(base_fare * distance_multiplier, 2)
    
    def accept_ride(self, driver_email):
        """Driver accepts the ride"""
        if self.status == "requested":
            self.driver_email = driver_email
            self.status = "accepted"
            self.accepted_at = datetime.now()
            return True
        return False
    
    def start_ride(self):
        """Driver starts the ride"""
        if self.status == "accepted":
            self.status = "started"
            self.started_at = datetime.now()
            return True
        return False
    
    def complete_ride(self):
        """Driver completes the ride"""
        if self.status == "started":
            self.status = "completed"
            self.completed_at = datetime.now()
            return True
        return False
    
    def cancel_ride(self):
        """Cancel the ride"""
        if self.status in ["requested", "accepted"]:
            self.status = "cancelled"
            return True
        return False
    
    def add_rating(self, rating):
        """Add rating to the ride"""
        if 1 <= rating <= 5:
            self.rating = rating
            return True
        return False
    
    def get_duration(self):
        """Get ride duration if completed"""
        if self.started_at and self.completed_at:
            duration = self.completed_at - self.started_at
            return duration.total_seconds() / 60  # in minutes
        return None
    
    def to_dict(self):
        """Convert ride to dictionary"""
        return {
            'ride_id': self.ride_id,
            'rider_email': self.rider_email,
            'driver_email': self.driver_email,
            'pickup_location': self.pickup_location,
            'drop_location': self.drop_location,
            'status': self.status,
            'requested_at': self.requested_at,
            'accepted_at': self.accepted_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'fare': self.fare,
            'rating': self.rating,
            'payment_status': self.payment_status
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create ride from dictionary"""
        ride = cls(data['pickup_location'], data['drop_location'])
        ride.ride_id = data['ride_id']
        ride.rider_email = data['rider_email']
        ride.driver_email = data.get('driver_email')
        ride.status = data['status']
        ride.requested_at = data['requested_at']
        ride.accepted_at = data.get('accepted_at')
        ride.started_at = data.get('started_at')
        ride.completed_at = data.get('completed_at')
        ride.fare = data['fare']
        ride.rating = data.get('rating')
        ride.payment_status = data.get('payment_status', 'pending')
        return ride
