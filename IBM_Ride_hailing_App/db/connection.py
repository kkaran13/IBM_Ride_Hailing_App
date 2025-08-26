import pymongo
from pymongo.errors import ConnectionFailure

class DatabaseConnection:
    def __init__(self):
        self.client = None
        self.db = None
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["rideapp"]
            # Test connection
            self.client.admin.command('ping')
            print("Connected to MongoDB successfully!")
            return True
        except ConnectionFailure:
            print("Failed to connect to MongoDB")
            return False
    
    def get_database(self):
        """Get database instance"""
        return self.db
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("Database connection closed")

# Global database instance
db_connection = DatabaseConnection()
