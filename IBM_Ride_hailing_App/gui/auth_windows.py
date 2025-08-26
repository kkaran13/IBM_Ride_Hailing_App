import tkinter as tk
from tkinter import ttk, messagebox
from gui.base_window import BaseWindow
from auth.auth_manager import AuthManager
from utils.validators import Validators

class LoginWindow(BaseWindow):
    def __init__(self, auth_manager, show_welcome=False):
        super().__init__("Login - Ride App")
        self.auth_manager = auth_manager
        self.show_welcome = show_welcome
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the login UI"""
        # Title
        title_label = self.create_title_label("Welcome Back!")
        title_label.pack(pady=(0, 10))
        
        # Welcome message for newly registered users
        if self.show_welcome:
            welcome_label = tk.Label(self.main_frame, 
                                   text="Account created successfully! Please login with your credentials.",
                                   font=('Arial', 10),
                                   fg='#28a745', bg='#f0f0f0')
            welcome_label.pack(pady=(0, 20))
        
        # Login form
        form_frame = self.create_frame()
        form_frame.pack(pady=20)
        
        # Email field
        email_frame, self.email_entry = self.create_entry_field("Email", form_frame)
        email_frame.pack(fill=tk.X, pady=10)
        
        # Password field
        password_frame, self.password_entry = self.create_entry_field("Password", form_frame, show="*")
        password_frame.pack(fill=tk.X, pady=10)
        
        # Login button
        login_button = self.create_button("Login", self.login, parent=form_frame)
        login_button.pack(fill=tk.X, pady=20)
        
        # Register link
        register_label = tk.Label(form_frame, text="Don't have an account? Register here", 
                                fg='#007bff', cursor='hand2', bg='#f0f0f0')
        register_label.pack(pady=10)
        register_label.bind("<Button-1>", lambda e: self.show_register())
    
    def login(self):
        """Handle login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            self.show_error("Please fill in all fields")
            return
        
        if not Validators.validate_email(email):
            self.show_error("Please enter a valid email")
            return
        
        success, message = self.auth_manager.login_user(email, password)
        if success:
            self.show_success(message)
            self.root.destroy()
            # Launch dashboard after successful login
            from gui.dashboard import Dashboard
            dashboard = Dashboard(self.auth_manager)
            dashboard.run()
        else:
            self.show_error(message)
    
    def show_register(self):
        """Show registration window"""
        self.root.destroy()
        register_window = RegisterWindow(self.auth_manager)
        register_window.run()

class RegisterWindow(BaseWindow):
    def __init__(self, auth_manager):
        super().__init__("Register - Ride App")
        self.auth_manager = auth_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the registration UI"""
        # Title
        title_label = self.create_title_label("Create Account")
        title_label.pack(pady=(0, 20))
        
        # Registration form
        form_frame = self.create_frame()
        form_frame.pack(pady=20)
        
        # Name field
        name_frame, self.name_entry = self.create_entry_field("Full Name", form_frame)
        name_frame.pack(fill=tk.X, pady=10)
        
        # Email field
        email_frame, self.email_entry = self.create_entry_field("Email", form_frame)
        email_frame.pack(fill=tk.X, pady=10)
        
        # Phone field
        phone_frame, self.phone_entry = self.create_entry_field("Phone Number", form_frame)
        phone_frame.pack(fill=tk.X, pady=10)
        
        # Password field
        password_frame, self.password_entry = self.create_entry_field("Password", form_frame, show="*")
        password_frame.pack(fill=tk.X, pady=10)
        
        # Confirm password field
        confirm_frame, self.confirm_entry = self.create_entry_field("Confirm Password", form_frame, show="*")
        confirm_frame.pack(fill=tk.X, pady=10)
        
        # User type selection
        type_frame = tk.Frame(form_frame, bg='#f0f0f0')
        type_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(type_frame, text="User Type:", font=('Arial', 10, 'bold'),
                fg='#333333', bg='#f0f0f0').pack(anchor='w')
        
        self.user_type = tk.StringVar(value="rider")
        rider_radio = tk.Radiobutton(type_frame, text="Rider", variable=self.user_type, 
                                   value="rider", bg='#f0f0f0')
        driver_radio = tk.Radiobutton(type_frame, text="Driver", variable=self.user_type, 
                                    value="driver", bg='#f0f0f0')
        rider_radio.pack(anchor='w')
        driver_radio.pack(anchor='w')
        
        # License number field (for drivers)
        self.license_frame, self.license_entry = self.create_entry_field("Driver License Number", form_frame)
        self.license_frame.pack(fill=tk.X, pady=10)
        self.license_frame.pack_forget()  # Hide initially
        
        # Show/hide license field based on user type
        self.user_type.trace('w', self.on_user_type_change)
        
        # Register button
        register_button = self.create_button("Register", self.register, parent=form_frame)
        register_button.pack(fill=tk.X, pady=20)
        
        # Login link
        login_label = tk.Label(form_frame, text="Already have an account? Login here", 
                             fg='#007bff', cursor='hand2', bg='#f0f0f0')
        login_label.pack(pady=10)
        login_label.bind("<Button-1>", lambda e: self.show_login())
    
    def on_user_type_change(self, *args):
        """Show/hide license field based on user type"""
        if self.user_type.get() == "driver":
            self.license_frame.pack(fill=tk.X, pady=10)
        else:
            self.license_frame.pack_forget()
    
    def register(self):
        """Handle registration"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        user_type = self.user_type.get()
        license_number = self.license_entry.get().strip() if user_type == "driver" else None
        
        # Validation
        if not all([name, email, phone, password, confirm]):
            self.show_error("Please fill in all fields")
            return
        
        if not Validators.validate_email(email):
            self.show_error("Please enter a valid email")
            return
        
        if not Validators.validate_phone(phone):
            self.show_error("Please enter a valid phone number")
            return
        
        if password != confirm:
            self.show_error("Passwords do not match")
            return
        
        is_valid, message = Validators.validate_password(password)
        if not is_valid:
            self.show_error(message)
            return
        
        if user_type == "driver" and not license_number:
            self.show_error("Driver license number is required")
            return
        
        if user_type == "driver" and not Validators.validate_license(license_number):
            self.show_error("Please enter a valid license number")
            return
        
        # Register user
        success, message = self.auth_manager.register_user(
            email, password, name, phone, user_type, license_number
        )
        
        if success:
            self.show_success("Registration successful! Redirecting to login...")
            # Wait a moment for the success message to be seen
            self.root.after(1500, self.show_login)
        else:
            self.show_error(message)
    
    def show_login(self):
        """Show login window"""
        self.root.destroy()
        login_window = LoginWindow(self.auth_manager, show_welcome=True)
        login_window.run()
