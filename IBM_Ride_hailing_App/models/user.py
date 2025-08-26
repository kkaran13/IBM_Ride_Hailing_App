from typing import final
from datetime import datetime

class User:
    def __init__(self, email, password, name, phone):
        self._email = email
        self._password = password
        self.name = name
        self.phone = phone
        self.created_at = datetime.now()
        self.rating = 0.0
        self.total_rides = 0
    
    # Getter and setter for email with validation
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if '@' in value and '.' in value:
            self._email = value
        else:
            raise ValueError("Invalid email format")
    
    # Getter and setter for password with validation
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        if len(value) >= 6:
            self._password = value
        else:
            raise ValueError("Password must be at least 6 characters")
    
    def to_dict(self):
        """Convert user to dictionary for database storage"""
        return {
            'email': self._email,
            'password': self._password,
            'name': self.name,
            'phone': self.phone,
            'created_at': self.created_at,
            'rating': self.rating,
            'total_rides': self.total_rides
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user from dictionary data"""
        user = cls(data['email'], data['password'], data['name'], data['phone'])
        user.created_at = data.get('created_at', datetime.now())
        user.rating = data.get('rating', 0.0)
        user.total_rides = data.get('total_rides', 0)
        return user

class Driver(User):
    def __init__(self, email, password, name, phone, license_number):
        super().__init__(email, password, name, phone)
        self.license_number = license_number
        self.vehicle = None
        self.is_available = True
        self.current_ride = None
    
    def add_vehicle(self, plate_number, vehicle_type, model):
        """Add vehicle information"""
        self.vehicle = {
            'plate_number': plate_number,
            'vehicle_type': vehicle_type,
            'model': model
        }
    
    def to_dict(self):
        """Convert driver to dictionary"""
        data = super().to_dict()
        data.update({
            'license_number': self.license_number,
            'vehicle': self.vehicle,
            'is_available': self.is_available,
            'current_ride': self.current_ride
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create driver from dictionary"""
        driver = cls(data['email'], data['password'], data['name'], 
                    data['phone'], data['license_number'])
        driver.vehicle = data.get('vehicle')
        driver.is_available = data.get('is_available', True)
        driver.current_ride = data.get('current_ride')
        driver.created_at = data.get('created_at', datetime.now())
        driver.rating = data.get('rating', 0.0)
        driver.total_rides = data.get('total_rides', 0)
        return driver

@final
class Rider(User):
    def __init__(self, email, password, name, phone):
        super().__init__(email, password, name, phone)
        self.payment_methods = []
        self.current_ride = None
    
    def add_payment_method(self, method):
        """Add a payment method"""
        if method not in self.payment_methods:
            self.payment_methods.append(method)
    
    def to_dict(self):
        """Convert rider to dictionary"""
        data = super().to_dict()
        data.update({
            'payment_methods': self.payment_methods,
            'current_ride': self.current_ride
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create rider from dictionary"""
        rider = cls(data['email'], data['password'], data['name'], data['phone'])
        rider.payment_methods = data.get('payment_methods', [])
        rider.current_ride = data.get('current_ride')
        rider.created_at = data.get('created_at', datetime.now())
        rider.rating = data.get('rating', 0.0)
        rider.total_rides = data.get('total_rides', 0)
        return rider
