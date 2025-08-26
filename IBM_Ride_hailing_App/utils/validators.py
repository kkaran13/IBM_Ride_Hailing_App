import re
from datetime import datetime

class Validators:
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number format"""
        # Remove spaces and special characters
        clean_phone = re.sub(r'[^\d]', '', phone)
        return len(clean_phone) >= 10
    
    @staticmethod
    def validate_license(license_number):
        """Validate driver license number format"""
        # Basic validation - can be customized based on country
        if len(license_number) < 5:
            return False
        return True
    
    @staticmethod
    def validate_vehicle_plate(plate_number):
        """Validate vehicle plate number"""
        if len(plate_number) < 4:
            return False
        return True
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        return True, "Password is valid"
    
    @staticmethod
    def format_phone(phone):
        """Format phone number for display"""
        clean_phone = re.sub(r'[^\d]', '', phone)
        if len(clean_phone) == 10:
            return f"({clean_phone[:3]}) {clean_phone[3:6]}-{clean_phone[6:]}"
        return phone
    
    @staticmethod
    def format_currency(amount):
        """Format amount as currency"""
        return f"${amount:.2f}"
    
    @staticmethod
    def format_datetime(dt):
        """Format datetime for display"""
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    
    @staticmethod
    def calculate_rating_average(ratings):
        """Calculate average rating from list of ratings"""
        if not ratings:
            return 0.0
        return sum(ratings) / len(ratings)
    
    @staticmethod
    def sanitize_input(text):
        """Sanitize user input"""
        if not text:
            return ""
        # Remove potentially dangerous characters
        return re.sub(r'[<>"\']', '', text.strip())
