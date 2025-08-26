from db.connection import db_connection
from models.user import User, Driver, Rider
import hashlib

class AuthManager:
    def __init__(self):
        self.db = db_connection.get_database()
        self.current_user = None
    
    def _hash_password(self, password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password, hashed):
        """Verify password hash"""
        return self._hash_password(password) == hashed
    
    def register_user(self, email, password, name, phone, user_type, license_number=None):
        """Register a new user"""
        try:
            # Check if email already exists
            if self.db.users.find_one({"email": email}):
                return False, "Email already registered"
            
            # Check if license number is unique for drivers
            if user_type == "driver" and license_number:
                if self.db.users.find_one({"license_number": license_number}):
                    return False, "License number already registered"
            
            # Hash password
            hashed_password = self._hash_password(password)
            
            # Create user object
            if user_type == "driver":
                user = Driver(email, hashed_password, name, phone, license_number)
            else:
                user = Rider(email, hashed_password, name, phone)
            
            # Save to database
            self.db.users.insert_one(user.to_dict())
            return True, "Registration successful"
            
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def login_user(self, email, password):
        """Login user"""
        try:
            # Find user in database
            user_data = self.db.users.find_one({"email": email})
            if not user_data:
                return False, "User not found"
            
            # Verify password
            if not self._verify_password(password, user_data["password"]):
                return False, "Invalid password"
            
            # Create user object
            if "license_number" in user_data:
                user = Driver.from_dict(user_data)
            else:
                user = Rider.from_dict(user_data)
            
            self.current_user = user
            return True, "Login successful"
            
        except Exception as e:
            return False, f"Login failed: {str(e)}"
    
    def logout_user(self):
        """Logout current user"""
        self.current_user = None
        return True, "Logout successful"
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.current_user is not None
    
    def update_user_rating(self, email, new_rating):
        """Update user rating"""
        try:
            result = self.db.users.update_one(
                {"email": email},
                {"$set": {"rating": new_rating}}
            )
            return result.modified_count > 0
        except Exception:
            return False
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            user_data = self.db.users.find_one({"email": email})
            if user_data:
                if "license_number" in user_data:
                    return Driver.from_dict(user_data)
                else:
                    return Rider.from_dict(user_data)
            return None
        except Exception:
            return None
