import tkinter as tk
from tkinter import ttk, messagebox
from gui.base_window import BaseWindow
from auth.auth_manager import AuthManager
from core.ride_manager import RideManager
from core.payment_manager import PaymentManager
from utils.validators import Validators

class Dashboard(BaseWindow):
    def __init__(self, auth_manager):
        super().__init__("Dashboard - Ride App", width=1000, height=700)
        self.auth_manager = auth_manager
        self.ride_manager = RideManager()
        self.payment_manager = PaymentManager()
        self.current_user = auth_manager.get_current_user()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dashboard UI"""
        # Header
        header_frame = self.create_header()
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Main content area
        self.content_frame = self.create_frame()
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Show appropriate interface based on user type
        if hasattr(self.current_user, 'license_number'):
            self.show_driver_interface()
        else:
            self.show_rider_interface()
    
    def create_header(self):
        """Create the header with user info and logout"""
        header_frame = tk.Frame(self.root, bg='#007bff', height=60)
        header_frame.pack_propagate(False)
        
        # User info
        user_info = tk.Label(header_frame, 
                           text=f"Welcome, {self.current_user.name}!",
                           font=('Arial', 14, 'bold'),
                           fg='white', bg='#007bff')
        user_info.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Logout button
        logout_btn = tk.Button(header_frame, text="Logout", 
                             command=self.logout,
                             font=('Arial', 10),
                             bg='#dc3545', fg='white',
                             relief=tk.FLAT, padx=15)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=15)
        
        return header_frame
    
    def show_rider_interface(self):
        """Show rider interface"""
        self.clear_widgets(self.content_frame)
        
        # Title
        title = self.create_title_label("Rider Dashboard", self.content_frame)
        title.pack(pady=(0, 20))
        
        # Request ride section
        ride_frame = self.create_frame(self.content_frame)
        ride_frame.pack(fill=tk.X, pady=10)
        
        ride_title = self.create_subtitle_label("Request a Ride", ride_frame)
        ride_title.pack(anchor='w')
        
        # Pickup and drop locations
        pickup_frame, self.pickup_entry = self.create_entry_field("Pickup Location", ride_frame)
        pickup_frame.pack(fill=tk.X, pady=5)
        
        drop_frame, self.drop_entry = self.create_entry_field("Drop Location", ride_frame)
        drop_frame.pack(fill=tk.X, pady=5)
        
        # Request button
        request_btn = self.create_button("Request Ride", self.request_ride, parent=ride_frame)
        request_btn.pack(fill=tk.X, pady=10)
        
        # Current rides section
        self.show_rider_rides()
    
    def show_driver_interface(self):
        """Show driver interface"""
        self.clear_widgets(self.content_frame)
        
        # Title
        title = self.create_title_label("Driver Dashboard", self.content_frame)
        title.pack(pady=(0, 20))
        
        # Vehicle info section
        if not self.current_user.vehicle:
            self.show_vehicle_registration()
        else:
            self.show_driver_rides()
    
    def show_vehicle_registration(self):
        """Show vehicle registration form"""
        vehicle_frame = self.create_frame(self.content_frame)
        vehicle_frame.pack(fill=tk.X, pady=10)
        
        vehicle_title = self.create_subtitle_label("Vehicle Registration", vehicle_frame)
        vehicle_title.pack(anchor='w')
        
        # Vehicle fields
        plate_frame, self.plate_entry = self.create_entry_field("License Plate Number", vehicle_frame)
        plate_frame.pack(fill=tk.X, pady=5)
        
        type_frame, self.type_entry = self.create_entry_field("Vehicle Type (e.g., Sedan, SUV)", vehicle_frame)
        type_frame.pack(fill=tk.X, pady=5)
        
        model_frame, self.model_entry = self.create_entry_field("Vehicle Model", vehicle_frame)
        model_frame.pack(fill=tk.X, pady=5)
        
        # Register button
        register_btn = self.create_button("Register Vehicle", self.register_vehicle, parent=vehicle_frame)
        register_btn.pack(fill=tk.X, pady=10)
    
    def register_vehicle(self):
        """Register vehicle for driver"""
        plate = self.plate_entry.get().strip()
        vehicle_type = self.type_entry.get().strip()
        model = self.model_entry.get().strip()
        
        if not all([plate, vehicle_type, model]):
            self.show_error("Please fill in all vehicle fields")
            return
        
        if not Validators.validate_vehicle_plate(plate):
            self.show_error("Please enter a valid license plate")
            return
        
        # Add vehicle to driver
        self.current_user.add_vehicle(plate, vehicle_type, model)
        
        # Update database
        from db.connection import db_connection
        db = db_connection.get_database()
        db.users.update_one(
            {"email": self.current_user.email},
            {"$set": {"vehicle": self.current_user.vehicle}}
        )
        
        self.show_success("Vehicle registered successfully!")
        self.show_driver_rides()
    
    def show_driver_rides(self):
        """Show available rides for driver"""
        # Available rides section
        rides_frame = self.create_frame(self.content_frame)
        rides_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        rides_title = self.create_subtitle_label("Available Rides", rides_frame)
        rides_title.pack(anchor='w')
        
        # Get available rides
        available_rides = self.ride_manager.get_available_rides()
        
        if not available_rides:
            no_rides = tk.Label(rides_frame, text="No rides available at the moment",
                              font=('Arial', 12), fg='#666666', bg='#f0f0f0')
            no_rides.pack(pady=20)
        else:
            # Create scrollable frame for rides
            canvas = tk.Canvas(rides_frame, bg='#f0f0f0')
            scrollbar = ttk.Scrollbar(rides_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Display rides
            for ride in available_rides:
                self.create_ride_card(ride, scrollable_frame, is_driver=True)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        
        # Current ride section
        if self.current_user.current_ride:
            self.show_current_ride()
    
    def show_rider_rides(self):
        """Show rider's current and past rides"""
        rides_frame = self.create_frame(self.content_frame)
        rides_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        rides_title = self.create_subtitle_label("Your Rides", rides_frame)
        rides_title.pack(anchor='w')
        
        # Get user rides
        user_rides = self.ride_manager.get_user_rides(self.current_user.email)
        
        if not user_rides:
            no_rides = tk.Label(rides_frame, text="No rides yet. Request your first ride!",
                              font=('Arial', 12), fg='#666666', bg='#f0f0f0')
            no_rides.pack(pady=20)
        else:
            # Create scrollable frame
            canvas = tk.Canvas(rides_frame, bg='#f0f0f0')
            scrollbar = ttk.Scrollbar(rides_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Display rides
            for ride in user_rides:
                self.create_ride_card(ride, scrollable_frame, is_driver=False)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
    
    def create_ride_card(self, ride, parent, is_driver):
        """Create a ride information card"""
        card_frame = tk.Frame(parent, relief=tk.RAISED, bd=2, bg='white')
        card_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Ride info
        info_frame = tk.Frame(card_frame, bg='white')
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(info_frame, text=f"Ride ID: {ride.ride_id}", 
                font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        tk.Label(info_frame, text=f"From: {ride.pickup_location}", bg='white').pack(anchor='w')
        tk.Label(info_frame, text=f"To: {ride.drop_location}", bg='white').pack(anchor='w')
        tk.Label(info_frame, text=f"Fare: {Validators.format_currency(ride.fare)}", bg='white').pack(anchor='w')
        tk.Label(info_frame, text=f"Status: {ride.status.title()}", bg='white').pack(anchor='w')
        
        # Action buttons
        button_frame = tk.Frame(card_frame, bg='white')
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        if is_driver and ride.status == "requested":
            accept_btn = tk.Button(button_frame, text="Accept Ride", 
                                 command=lambda: self.accept_ride(ride.ride_id),
                                 bg='#28a745', fg='white', relief=tk.FLAT)
            accept_btn.pack(side=tk.LEFT, padx=(0, 10))
        elif is_driver and ride.status == "accepted" and ride.driver_email == self.current_user.email:
            start_btn = tk.Button(button_frame, text="Start Ride", 
                                command=lambda: self.start_ride(ride.ride_id),
                                bg='#007bff', fg='white', relief=tk.FLAT)
            start_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            complete_btn = tk.Button(button_frame, text="Complete Ride", 
                                   command=lambda: self.complete_ride(ride.ride_id),
                                   bg='#28a745', fg='white', relief=tk.FLAT)
            complete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        if ride.status in ["requested", "accepted"]:
            cancel_btn = tk.Button(button_frame, text="Cancel Ride", 
                                 command=lambda: self.cancel_ride(ride.ride_id),
                                 bg='#dc3545', fg='white', relief=tk.FLAT)
            cancel_btn.pack(side=tk.LEFT)
        
        if ride.status == "completed" and not ride.rating:
            self.create_rating_widget(ride, button_frame)
    
    def create_rating_widget(self, ride, parent):
        """Create rating widget for completed rides"""
        rating_frame = tk.Frame(parent, bg='white')
        rating_frame.pack(side=tk.RIGHT)
        
        tk.Label(rating_frame, text="Rate:", bg='white').pack(side=tk.LEFT)
        
        rating_var = tk.StringVar(value="5")
        rating_combo = ttk.Combobox(rating_frame, textvariable=rating_var, 
                                   values=["1", "2", "3", "4", "5"], width=5)
        rating_combo.pack(side=tk.LEFT, padx=5)
        
        rate_btn = tk.Button(rating_frame, text="Submit Rating", 
                           command=lambda: self.submit_rating(ride.ride_id, int(rating_var.get())),
                           bg='#007bff', fg='white', relief=tk.FLAT)
        rate_btn.pack(side=tk.LEFT)
    
    def request_ride(self):
        """Request a new ride"""
        pickup = self.pickup_entry.get().strip()
        drop = self.drop_entry.get().strip()
        
        if not pickup or not drop:
            self.show_error("Please enter pickup and drop locations")
            return
        
        success, ride_id, message = self.ride_manager.request_ride(
            self.current_user.email, pickup, drop
        )
        
        if success:
            self.show_success(f"Ride requested! Ride ID: {ride_id}")
            self.pickup_entry.delete(0, tk.END)
            self.drop_entry.delete(0, tk.END)
            self.show_rider_rides()
        else:
            self.show_error(message)
    
    def accept_ride(self, ride_id):
        """Driver accepts a ride"""
        success, message = self.ride_manager.accept_ride(ride_id, self.current_user.email)
        if success:
            self.show_success(message)
            self.show_driver_rides()
        else:
            self.show_error(message)
    
    def start_ride(self, ride_id):
        """Driver starts a ride"""
        success, message = self.ride_manager.start_ride(ride_id, self.current_user.email)
        if success:
            self.show_success(message)
            self.show_driver_rides()
        else:
            self.show_error(message)
    
    def complete_ride(self, ride_id):
        """Driver completes a ride"""
        success, message = self.ride_manager.complete_ride(ride_id, self.current_user.email)
        if success:
            self.show_success(message)
            self.show_driver_rides()
        else:
            self.show_error(message)
    
    def cancel_ride(self, ride_id):
        """Cancel a ride"""
        success, message = self.ride_manager.cancel_ride(ride_id, self.current_user.email)
        if success:
            self.show_success(message)
            if hasattr(self.current_user, 'license_number'):
                self.show_driver_rides()
            else:
                self.show_rider_rides()
        else:
            self.show_error(message)
    
    def submit_rating(self, ride_id, rating):
        """Submit rating for a ride"""
        success, message = self.ride_manager.rate_ride(ride_id, rating)
        if success:
            self.show_success(message)
            if hasattr(self.current_user, 'license_number'):
                self.show_driver_rides()
            else:
                self.show_rider_rides()
        else:
            self.show_error(message)
    
    def show_current_ride(self):
        """Show current ride information"""
        current_ride = self.ride_manager.get_ride_by_id(self.current_user.current_ride)
        if current_ride:
            current_frame = self.create_frame(self.content_frame)
            current_frame.pack(fill=tk.X, pady=10)
            
            current_title = self.create_subtitle_label("Current Ride", current_frame)
            current_title.pack(anchor='w')
            
            # Show current ride details
            tk.Label(current_frame, text=f"Ride ID: {current_ride.ride_id}", bg='#f0f0f0').pack(anchor='w')
            tk.Label(current_frame, text=f"Status: {current_ride.status.title()}", bg='#f0f0f0').pack(anchor='w')
            tk.Label(current_frame, text=f"Fare: {Validators.format_currency(current_ride.fare)}", bg='#f0f0f0').pack(anchor='w')
    
    def logout(self):
        """Logout user"""
        self.auth_manager.logout_user()
        self.root.destroy()
        # Return to login
        from gui.auth_windows import LoginWindow
        login_window = LoginWindow(self.auth_manager, show_welcome=False)
        login_window.run()
