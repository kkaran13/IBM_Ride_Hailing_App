#!/usr/bin/env python3
"""
Demo script for the Ride App
Shows how to use the app programmatically
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_user_creation():
    """Demonstrate user creation"""
    print("=== USER CREATION DEMO ===")
    
    try:
        from models.user import User, Driver, Rider
        
        # Create a rider
        rider = Rider("john@example.com", "password123", "John Rider", "555-0101")
        print(f"Created rider: {rider.name} ({rider.email})")
        
        # Create a driver
        driver = Driver("jane@example.com", "password123", "Jane Driver", "555-0102", "DL12345")
        print(f"Created driver: {driver.name} ({driver.email})")
        
        # Add vehicle to driver
        driver.add_vehicle("ABC123", "Sedan", "Toyota Camry")
        print(f"Driver vehicle: {driver.vehicle['model']} {driver.vehicle['vehicle_type']}")
        
        print("✓ User creation demo completed!\n")
        return True
        
    except Exception as e:
        print(f"✗ User creation demo failed: {e}")
        return False

def demo_ride_management():
    """Demonstrate ride management"""
    print("=== RIDE MANAGEMENT DEMO ===")
    
    try:
        from models.ride import Ride
        
        # Create a ride
        ride = Ride("john@example.com", "Central Park", "Times Square")
        print(f"Created ride: {ride.ride_id}")
        print(f"Status: {ride.status}")
        print(f"Fare: ${ride.fare}")
        
        # Driver accepts ride
        if ride.accept_ride("jane@example.com"):
            print("Driver accepted the ride")
            print(f"Status: {ride.status}")
        
        # Start the ride
        if ride.start_ride():
            print("Ride started")
            print(f"Status: {ride.status}")
        
        # Complete the ride
        if ride.complete_ride():
            print("Ride completed")
            print(f"Status: {ride.status}")
            print(f"Duration: {ride.get_duration()} minutes")
        
        # Rate the ride
        if ride.add_rating(5):
            print("Ride rated: 5 stars")
        
        print("✓ Ride management demo completed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Ride management demo failed: {e}")
        return False

def demo_validation():
    """Demonstrate validation features"""
    print("=== VALIDATION DEMO ===")
    
    try:
        from utils.validators import Validators
        
        # Test email validation
        test_emails = ["valid@email.com", "invalid-email", "another@test.org"]
        for email in test_emails:
            is_valid = Validators.validate_email(email)
            print(f"Email '{email}': {'✓ Valid' if is_valid else '✗ Invalid'}")
        
        # Test password validation
        test_passwords = ["short", "longpassword", "123456"]
        for password in test_passwords:
            is_valid, message = Validators.validate_password(password)
            print(f"Password '{password}': {'✓ Valid' if is_valid else '✗ Invalid'} - {message}")
        
        # Test phone validation
        test_phones = ["1234567890", "123", "(555) 123-4567"]
        for phone in test_phones:
            is_valid = Validators.validate_phone(phone)
            print(f"Phone '{phone}': {'✓ Valid' if is_valid else '✗ Invalid'}")
        
        print("✓ Validation demo completed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Validation demo failed: {e}")
        return False

def demo_location_features():
    """Demonstrate location features"""
    print("=== LOCATION FEATURES DEMO ===")
    
    try:
        from utils.location_utils import LocationUtils
        
        # Get sample locations
        locations = LocationUtils.get_sample_locations()
        print(f"Sample locations available: {len(locations)}")
        for i, location in enumerate(locations[:3], 1):
            print(f"  {i}. {location}")
        
        # Test distance estimation
        pickup = "Central Park, New York"
        drop = "Times Square, New York"
        distance = LocationUtils.get_distance_estimate(pickup, drop)
        fare = LocationUtils.get_estimated_fare(pickup, drop)
        
        print(f"\nRoute: {pickup} → {drop}")
        print(f"Estimated distance: {distance} miles")
        print(f"Estimated fare: ${fare}")
        
        print("✓ Location features demo completed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Location features demo failed: {e}")
        return False

def demo_polymorphism():
    """Demonstrate OOP concepts"""
    print("=== OOP CONCEPTS DEMO ===")
    
    try:
        from models.user import User, Driver, Rider
        
        # Create different user types
        users = [
            User("admin@example.com", "password", "Admin User", "555-0000"),
            Driver("driver@example.com", "password", "Driver User", "555-0001", "DL00001"),
            Rider("rider@example.com", "password", "Rider User", "555-0002")
        ]
        
        # Demonstrate polymorphism
        for user in users:
            print(f"User: {user.name}")
            print(f"  Type: {type(user).__name__}")
            print(f"  Email: {user.email}")  # Using getter
            print(f"  Total rides: {user.total_rides}")
            
            # Demonstrate inheritance
            if isinstance(user, Driver):
                print(f"  License: {user.license_number}")
                print(f"  Available: {user.is_available}")
            elif isinstance(user, Rider):
                print(f"  Payment methods: {user.payment_methods}")
            
            print()
        
        print("✓ OOP concepts demo completed!\n")
        return True
        
    except Exception as e:
        print(f"✗ OOP concepts demo failed: {e}")
        return False

def main():
    """Run all demos"""
    print("🚗 RIDE APP DEMONSTRATION 🚗\n")
    
    demos = [
        demo_user_creation,
        demo_ride_management,
        demo_validation,
        demo_location_features,
        demo_polymorphism
    ]
    
    passed = 0
    total = len(demos)
    
    for demo in demos:
        if demo():
            passed += 1
    
    print("=== DEMO RESULTS ===")
    print(f"Successful demos: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All demos completed successfully!")
        print("\nThe app demonstrates:")
        print("✓ User registration and authentication")
        print("✓ Ride management (request, accept, start, complete)")
        print("✓ Input validation and error handling")
        print("✓ Location utilities and Google Maps integration")
        print("✓ Object-oriented programming concepts")
        print("✓ Database operations with MongoDB")
        print("✓ Clean, modular code structure")
        
        print("\nTo run the full GUI application:")
        print("1. Make sure MongoDB is running")
        print("2. Install requirements: pip install -r requirements.txt")
        print("3. Run: python main.py")
    else:
        print("\n❌ Some demos failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
