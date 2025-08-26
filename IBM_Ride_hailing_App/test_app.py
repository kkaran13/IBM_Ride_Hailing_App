#!/usr/bin/env python3
"""
Simple test script for the Ride App
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_models():
    """Test the model classes"""
    print("Testing models...")
    
    try:
        from models.user import User, Driver, Rider
        from models.ride import Ride
        
        # Test User class
        user = User("test@example.com", "password123", "Test User", "1234567890")
        print(f"✓ User created: {user.name}")
        
        # Test Driver class
        driver = Driver("driver@example.com", "password123", "Test Driver", "1234567890", "DL12345")
        print(f"✓ Driver created: {driver.name}")
        
        # Test Rider class
        rider = Rider("rider@example.com", "password123", "Test Rider", "1234567890")
        print(f"✓ Rider created: {rider.name}")
        
        # Test Ride class
        ride = Ride("rider@example.com", "Central Park", "Times Square")
        print(f"✓ Ride created: {ride.ride_id}")
        
        print("✓ All models working correctly!")
        return True
        
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def test_validators():
    """Test the validator functions"""
    print("\nTesting validators...")
    
    try:
        from utils.validators import Validators
        
        # Test email validation
        assert Validators.validate_email("test@example.com") == True
        assert Validators.validate_email("invalid-email") == False
        print("✓ Email validation working")
        
        # Test phone validation
        assert Validators.validate_phone("1234567890") == True
        assert Validators.validate_phone("123") == False
        print("✓ Phone validation working")
        
        # Test password validation
        is_valid, message = Validators.validate_password("short")
        assert is_valid == False
        is_valid, message = Validators.validate_password("longpassword")
        assert is_valid == True
        print("✓ Password validation working")
        
        print("✓ All validators working correctly!")
        return True
        
    except Exception as e:
        print(f"✗ Validator test failed: {e}")
        return False

def test_location_utils():
    """Test location utilities"""
    print("\nTesting location utilities...")
    
    try:
        from utils.location_utils import LocationUtils
        
        # Test location validation
        assert LocationUtils.validate_location("Central Park") == True
        assert LocationUtils.validate_location("") == False
        print("✓ Location validation working")
        
        # Test sample locations
        locations = LocationUtils.get_sample_locations()
        assert len(locations) > 0
        print(f"✓ Sample locations available: {len(locations)}")
        
        # Test distance estimation
        distance = LocationUtils.get_distance_estimate("Central Park", "Times Square")
        assert distance > 0
        print(f"✓ Distance estimation working: {distance} miles")
        
        print("✓ All location utilities working correctly!")
        return True
        
    except Exception as e:
        print(f"✗ Location utilities test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== RIDE APP TEST SUITE ===\n")
    
    tests = [
        test_models,
        test_validators,
        test_location_utils
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== TEST RESULTS ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The app is ready to run.")
        print("\nTo run the app:")
        print("1. Make sure MongoDB is running")
        print("2. Install requirements: pip install -r requirements.txt")
        print("3. Run: python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
