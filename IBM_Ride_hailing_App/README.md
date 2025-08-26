# IBM Ride Hailing App

A simple ride-hailing application built with Python, Tkinter, and MongoDB.

## Features
- User registration and login (Riders and Drivers)
- Driver license verification
- Vehicle registration for drivers
- Ride requests and acceptance
- Ride tracking with timestamps
- Payment simulation
- Rating system
- Basic role-based access control

## Setup
1. Install Python 3.8+
2. Install required packages: `pip install pymongo`
3. Make sure MongoDB is running locally
4. Run `python main.py`

## Project Structure
- `db/` - Database connection and operations
- `models/` - Data models and classes
- `auth/` - Authentication logic
- `core/` - Core business logic
- `gui/` - Tkinter GUI components
- `utils/` - Helper functions
- `main.py` - Main application entry point

## How to Use
1. Start the app
2. Register as a rider or driver
3. For drivers: add vehicle details
4. Request rides (riders) or accept rides (drivers)
5. Complete rides and rate each other
