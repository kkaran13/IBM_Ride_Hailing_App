import tkinter as tk
from tkinter import ttk, messagebox

class BaseWindow:
    def __init__(self, title="Ride App", width=800, height=600):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg='#f0f0f0')
        
        # Center the window
        self.center_window()
        
        # Configure styles
        self.setup_styles()
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def setup_styles(self):
        """Setup common styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton', 
                       background='#007bff', 
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Success.TButton', 
                       background='#28a745', 
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Danger.TButton', 
                       background='#dc3545', 
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        # Configure label styles
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       foreground='#333333')
        
        style.configure('Subtitle.TLabel', 
                       font=('Arial', 12, 'bold'),
                       foreground='#666666')
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
    
    def create_title_label(self, text, parent=None):
        """Create a title label"""
        if parent is None:
            parent = self.main_frame
        
        label = tk.Label(parent, text=text, 
                        font=('Arial', 18, 'bold'),
                        fg='#333333', bg='#f0f0f0')
        return label
    
    def create_subtitle_label(self, text, parent=None):
        """Create a subtitle label"""
        if parent is None:
            parent = self.main_frame
        
        label = tk.Label(parent, text=text, 
                        font=('Arial', 12),
                        fg='#666666', bg='#f0f0f0')
        return label
    
    def create_entry_field(self, label_text, parent=None, show=None):
        """Create a labeled entry field"""
        if parent is None:
            parent = self.main_frame
        
        frame = tk.Frame(parent, bg='#f0f0f0')
        
        label = tk.Label(frame, text=label_text, 
                        font=('Arial', 10, 'bold'),
                        fg='#333333', bg='#f0f0f0')
        label.pack(anchor='w')
        
        entry = tk.Entry(frame, font=('Arial', 10), 
                        relief=tk.SOLID, bd=1,
                        show=show)
        entry.pack(fill=tk.X, pady=(5, 0))
        
        return frame, entry
    
    def create_button(self, text, command, style='Primary.TButton', parent=None):
        """Create a styled button"""
        if parent is None:
            parent = self.main_frame
        
        button = ttk.Button(parent, text=text, command=command, style=style)
        return button
    
    def create_frame(self, parent=None, relief=tk.FLAT, bd=0):
        """Create a frame with common styling"""
        if parent is None:
            parent = self.main_frame
        
        frame = tk.Frame(parent, relief=relief, bd=bd, bg='#f0f0f0')
        return frame
    
    def show_message(self, title, message, message_type="info"):
        """Show a message box"""
        if message_type == "error":
            messagebox.showerror(title, message)
        elif message_type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
    
    def show_error(self, message):
        """Show error message"""
        self.show_message("Error", message, "error")
    
    def show_success(self, message):
        """Show success message"""
        self.show_message("Success", message, "info")
    
    def clear_widgets(self, parent=None):
        """Clear all widgets from a parent"""
        if parent is None:
            parent = self.main_frame
        
        for widget in parent.winfo_children():
            widget.destroy()
    
    def run(self):
        """Run the main loop"""
        self.root.mainloop()
    
    def close(self):
        """Close the window"""
        self.root.destroy()
