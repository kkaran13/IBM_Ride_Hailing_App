"""
Simple analytics module for ride app data visualization
"""

try:
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not available. Analytics features will be limited.")

class Analytics:
    def __init__(self, db_connection):
        self.db = db_connection.get_database()
    
    def get_user_ratings(self):
        """Get all user ratings for analysis"""
        try:
            users = list(self.db.users.find({}, {"rating": 1, "total_rides": 1}))
            ratings = [user.get("rating", 0) for user in users if user.get("rating", 0) > 0]
            return ratings
        except Exception:
            return []
    
    def get_ride_status_distribution(self):
        """Get distribution of ride statuses"""
        try:
            pipeline = [
                {"$group": {"_id": "$status", "count": {"$sum": 1}}}
            ]
            result = list(self.db.rides.aggregate(pipeline))
            return {item["_id"]: item["count"] for item in result}
        except Exception:
            return {}
    
    def get_monthly_rides(self, year):
        """Get monthly ride counts for a year"""
        try:
            pipeline = [
                {"$match": {"requested_at": {"$gte": f"{year}-01-01", "$lt": f"{year+1}-01-01"}}},
                {"$group": {"_id": {"$month": "$requested_at"}, "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ]
            result = list(self.db.rides.aggregate(pipeline))
            return {item["_id"]: item["count"] for item in result}
        except Exception:
            return {}
    
    def plot_ratings_distribution(self):
        """Plot distribution of user ratings"""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available for plotting")
            return
        
        ratings = self.get_user_ratings()
        if not ratings:
            print("No ratings data available")
            return
        
        plt.figure(figsize=(8, 6))
        plt.hist(ratings, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Distribution of User Ratings')
        plt.xlabel('Rating')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def plot_ride_status_distribution(self):
        """Plot distribution of ride statuses"""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available for plotting")
            return
        
        status_data = self.get_ride_status_distribution()
        if not status_data:
            print("No ride status data available")
            return
        
        labels = list(status_data.keys())
        values = list(status_data.values())
        
        plt.figure(figsize=(8, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Ride Status Distribution')
        plt.axis('equal')
        plt.show()
    
    def plot_monthly_rides(self, year):
        """Plot monthly ride counts for a year"""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available for plotting")
            return
        
        monthly_data = self.get_monthly_rides(year)
        if not monthly_data:
            print(f"No ride data available for {year}")
            return
        
        months = list(range(1, 13))
        counts = [monthly_data.get(month, 0) for month in months]
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        plt.figure(figsize=(10, 6))
        plt.bar(month_names, counts, color='lightgreen', alpha=0.7)
        plt.title(f'Monthly Ride Counts - {year}')
        plt.xlabel('Month')
        plt.ylabel('Number of Rides')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def generate_summary_report(self):
        """Generate a text summary report"""
        try:
            total_users = self.db.users.count_documents({})
            total_rides = self.db.rides.count_documents({})
            completed_rides = self.db.rides.count_documents({"status": "completed"})
            
            # Calculate average rating
            pipeline = [
                {"$match": {"rating": {"$exists": True, "$gt": 0}}},
                {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}}}
            ]
            rating_result = list(self.db.rides.aggregate(pipeline))
            avg_rating = rating_result[0]["avg_rating"] if rating_result else 0
            
            report = f"""
=== RIDE APP SUMMARY REPORT ===
Total Users: {total_users}
Total Rides: {total_rides}
Completed Rides: {completed_rides}
Completion Rate: {(completed_rides/total_rides*100):.1f}% (if total > 0)
Average Rating: {avg_rating:.2f}/5.0
===============================
            """
            return report.strip()
        except Exception as e:
            return f"Error generating report: {e}"
