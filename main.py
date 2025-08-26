#!/usr/bin/env python3
"""
IBM Ride Hailing App
Main application entry point
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.connection import db_connection
from auth.auth_manager import AuthManager
from gui.auth_windows import LoginWindow

def main():
    """Main application function"""
    print("Starting IBM Ride Hailing App...")
    
    # Connect to database
    if not db_connection.connect():
        print("Failed to connect to database. Please make sure MongoDB is running.")
        input("Press Enter to exit...")
        return
    
    try:
        # Initialize auth manager
        auth_manager = AuthManager()
        
        # Start with login window
        print("Starting login window...")
        login_window = LoginWindow(auth_manager, show_welcome=False)
        login_window.run()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
    
    finally:
        # Close database connection
        db_connection.close()
        print("Application closed.")

if __name__ == "__main__":
    main()
