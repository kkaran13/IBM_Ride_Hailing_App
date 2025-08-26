from db.connection import db_connection
from datetime import datetime

class PaymentManager:
    def __init__(self):
        self.db = db_connection.get_database()
        self.payment_methods = ["Credit Card", "Debit Card", "Cash", "Digital Wallet"]
    
    def process_payment(self, ride_id, amount, payment_method, user_email):
        """Process payment for a ride"""
        try:
            # Validate payment method
            if payment_method not in self.payment_methods:
                return False, "Invalid payment method"
            
            # Create payment record
            payment_data = {
                "ride_id": ride_id,
                "amount": amount,
                "payment_method": payment_method,
                "user_email": user_email,
                "status": "completed",
                "timestamp": datetime.now()
            }
            
            # Save payment to database
            self.db.payments.insert_one(payment_data)
            
            # Update ride payment status
            self.db.rides.update_one(
                {"ride_id": ride_id},
                {"$set": {"payment_status": "completed"}}
            )
            
            return True, "Payment processed successfully"
            
        except Exception as e:
            return False, f"Payment failed: {str(e)}"
    
    def get_payment_history(self, user_email):
        """Get payment history for a user"""
        try:
            payments = list(self.db.payments.find({"user_email": user_email}))
            return payments
        except Exception:
            return []
    
    def get_payment_methods(self):
        """Get available payment methods"""
        return self.payment_methods
    
    def get_total_earnings(self, driver_email):
        """Get total earnings for a driver"""
        try:
            # Get all completed rides for driver
            rides = list(self.db.rides.find({
                "driver_email": driver_email,
                "status": "completed"
            }))
            
            total = sum(ride["fare"] for ride in rides)
            return total
        except Exception:
            return 0.0
    
    def get_monthly_earnings(self, driver_email, year, month):
        """Get monthly earnings for a driver"""
        try:
            rides = list(self.db.rides.find({
                "driver_email": driver_email,
                "status": "completed",
                "completed_at": {
                    "$gte": datetime(year, month, 1),
                    "$lt": datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
                }
            }))
            
            total = sum(ride["fare"] for ride in rides)
            return total
        except Exception:
            return 0.0
