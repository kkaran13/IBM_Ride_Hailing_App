import tkinter as tk
from tkinter import ttk, messagebox
from gui.base_window import BaseWindow
from core.ride_manager import RideManager
from core.payment_manager import PaymentManager
from utils.validators import Validators


class Dashboard(BaseWindow):
    """Tabbed, scrollable Rider & Driver dashboards with auto-refresh and status."""

    # --- config ---
    AUTO_REFRESH_MS = 3000  # periodic refresh to reflect server-side changes

    def __init__(self, auth_manager):
        super().__init__("Dashboard - Ride App", width=1100, height=720)
        self.auth_manager = auth_manager
        self.ride_manager = RideManager()
        self.payment_manager = PaymentManager()
        self.current_user = auth_manager.get_current_user()

        # state holders
        self._mousewheel_bound_canvases = set()
        self.status_var = tk.StringVar(value="Online")
        self.notebook = None


        self.setup_styles()
        self.setup_ui()
        # start periodic refresh loop (reflect accept/complete/cancel made by others)
        # self.root.after(self.AUTO_REFRESH_MS, self._auto_refresh)

    # =============================
    # Styling
    # =============================
    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TNotebook", tabposition='n')
        style.configure("TNotebook.Tab", padding=(18, 10), font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#ffffff")])
        style.configure("Card.TFrame", background="white", relief="raised", borderwidth=1)
        style.configure("Section.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("SmallMut.TLabel", foreground="#666666")
        style.configure("Primary.TButton", padding=8)

    # =============================
    # UI skeleton
    # =============================
    def create_frame(self):
        return tk.Frame(self.root, bg="#f7f7f7")

    def setup_ui(self):
        header = self.create_header()
        header.pack(side=tk.TOP, fill=tk.X)  # no pady → no extra gap
        header.lift()

        self.content_frame = tk.Frame(self.root, bg="#f7f7f7")
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        if hasattr(self.current_user, 'license_number'):
            self.build_driver_tabs()
        else:
            self.build_rider_tabs()


    def create_header(self):
        header = tk.Frame(self.root, bg="#0d6efd", height=64)
        header.pack_propagate(False)

        left = tk.Frame(header, bg="#0d6efd")
        left.pack(side=tk.LEFT, padx=20)

        welcome = tk.Label(
            left,
            text=f"Welcome, {getattr(self.current_user, 'name', 'User')}!",
            font=("Segoe UI", 14, "bold"), fg="white", bg="#0d6efd"
        )
        welcome.pack(anchor="w", pady=16)

        right = tk.Frame(header, bg="#0d6efd")
        right.pack(side=tk.RIGHT, padx=20)

        # Driver status chip if driver
        if hasattr(self.current_user, 'license_number'):
            self.status_badge = tk.Label(
                right, textvariable=self.status_var, bg="#198754", fg="white",
                font=("Segoe UI", 10, "bold"), padx=10, pady=6
            )
            self.status_badge.pack(side=tk.RIGHT, padx=(0, 12), pady=12)

        logout_btn = tk.Button(
            right, text="Logout", command=self.logout,
            font=("Segoe UI", 10), bg="#dc3545", fg="white", relief=tk.FLAT, padx=16
        )
        logout_btn.pack(side=tk.RIGHT, pady=12)

        refresh_btn = tk.Button(
            right, text="Refresh", command=self.refresh_page,
            font=("Segoe UI", 10), bg="#f0f0f0", fg="black", relief=tk.FLAT, padx=16
        )
        refresh_btn.pack(side=tk.RIGHT, padx=(0, 12), pady=12)

        return header

    # =============================
    # Helpers: scrollable container & cards
    # =============================
    def make_scrollable(self, parent):
        """Create a vertical scrollable frame with mouse-wheel binding."""
        container = tk.Frame(parent, bg="#f7f7f7")
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg="#f7f7f7", highlightthickness=0)
        vs = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vs.set)

        inner = tk.Frame(canvas, bg="#f7f7f7")
        inner_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # resize content width to canvas width
            canvas.itemconfig(inner_id, width=canvas.winfo_width())
        inner.bind("<Configure>", _on_configure)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vs.pack(side=tk.RIGHT, fill=tk.Y)

        self._bind_mousewheel(canvas)
        return inner

    def _bind_mousewheel(self, canvas):
        if canvas in self._mousewheel_bound_canvases:
            return
        self._mousewheel_bound_canvases.add(canvas)

        def _on_mouse_wheel(event):
            # Windows / Mac uses event.delta, Linux often uses Button-4/5
            delta = 0
            if hasattr(event, 'delta') and event.delta:
                delta = int(-1 * (event.delta / 120))
            elif getattr(event, 'num', None) == 5:
                delta = 1
            elif getattr(event, 'num', None) == 4:
                delta = -1
            if delta:
                canvas.yview_scroll(delta, "units")

        canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
        canvas.bind_all("<Button-4>", _on_mouse_wheel)
        canvas.bind_all("<Button-5>", _on_mouse_wheel)

    def ride_card(self, parent, ride, actions):
        """Reusable ride card. actions: list[(label, callback, style_tag)]"""
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.X, padx=8, pady=6)

        body = tk.Frame(card, bg="white")
        body.pack(fill=tk.X, padx=12, pady=12)

        # left info
        info = tk.Frame(body, bg="white")
        info.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(info, text=f"Ride ID: {getattr(ride, 'ride_id', '')}",
                 bg="white", font=("Segoe UI", 10, "bold")).pack(anchor='w')
        tk.Label(info, text=f"From: {getattr(ride, 'pickup_location', '')}", bg="white").pack(anchor='w')
        tk.Label(info, text=f"To: {getattr(ride, 'drop_location', '')}", bg="white").pack(anchor='w')
        fare = getattr(ride, 'fare', 0)
        try:
            fare_text = Validators.format_currency(fare)
        except Exception:
            fare_text = str(fare)
        tk.Label(info, text=f"Fare: {fare_text}", bg="white").pack(anchor='w')
        tk.Label(info, text=f"Status: {getattr(ride, 'status', '').title()}", bg="white").pack(anchor='w')

        # right actions
        act = tk.Frame(body, bg="white")
        act.pack(side=tk.RIGHT)
        for (label, cb, style_tag) in actions:
            btn = tk.Button(
                act, text=label, command=cb,
                bg=style_tag.get('bg', '#0d6efd'), fg=style_tag.get('fg', 'white'),
                relief=tk.FLAT, padx=12, pady=6
            )
            btn.pack(side=tk.LEFT, padx=6)

    # =============================
    # Rider Dashboard
    # =============================
    def build_rider_tabs(self):
        self.clear_widgets(self.content_frame)
        title = ttk.Label(self.content_frame, text="Rider Dashboard", style="Title.TLabel")
        title.pack(pady=(0, 8))

        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Tab 1: Request Ride
        self.tab_request = tk.Frame(self.notebook, bg="#f7f7f7")
        self.notebook.add(self.tab_request, text="Request Ride")
        self._build_rider_request_tab(self.tab_request)

        # Tab 2: Requested Rides (incl. Accepted/Ongoing until completed)
        self.tab_requested = tk.Frame(self.notebook, bg="#f7f7f7")
        self.notebook.add(self.tab_requested, text="Requested Rides")

        # Tab 3: Completed Rides
        self.tab_completed = tk.Frame(self.notebook, bg="#f7f7f7")
        self.notebook.add(self.tab_completed, text="Completed Rides")

        self.refresh_rider_tabs()

    def _build_rider_request_tab(self, parent):
        section = tk.Frame(parent, bg="#f7f7f7")
        section.pack(fill=tk.X, padx=16, pady=16)

        ttk.Label(section, text="Request a Ride", style="Section.TLabel").pack(anchor='w', pady=(0, 8))

        row1, self.pickup_entry = self.create_entry_field("Pickup Location", section)
        row1.pack(fill=tk.X, pady=6)
        row2, self.drop_entry = self.create_entry_field("Drop Location", section)
        row2.pack(fill=tk.X, pady=6)

        req_btn = tk.Button(section, text="Request Ride", bg="#0d6efd", fg="white", relief=tk.FLAT,
                            padx=12, pady=8, command=self.request_ride)
        req_btn.pack(anchor='e', pady=(8, 0))

    def refresh_rider_tabs(self):
        # Requested tab
        for w in self.tab_requested.winfo_children():
            w.destroy()
        requested_wrap = self.make_scrollable(self.tab_requested)

        rides = self.ride_manager.get_user_rides(self.current_user.email)
        # requested & accepted show here until completed
        filtered = [r for r in rides if getattr(r, 'status', '') in ("requested", "accepted", "ongoing")]

        if not filtered:
            tk.Label(requested_wrap, text="No requested rides yet.", bg="#f7f7f7",
                     fg="#666").pack(pady=24)
        else:
            for r in filtered:
                actions = []
                if getattr(r, 'status', '') in ("accepted", "ongoing"):
                    actions.append((
                        "Complete Ride",
                        lambda rid=r.ride_id: self.complete_ride_rider(rid),
                        {"bg": "#198754"}
                    ))
                if getattr(r, 'status', '') in ("requested", "accepted", "ongoing"):
                    actions.append((
                        "Cancel Ride",
                        lambda rid=r.ride_id: self.cancel_ride(rid),
                        {"bg": "#dc3545"}
                    ))
                self.ride_card(requested_wrap, r, actions)

        # Completed tab
        for w in self.tab_completed.winfo_children():
            w.destroy()
        completed_wrap = self.make_scrollable(self.tab_completed)

        completed = [r for r in rides if getattr(r, 'status', '') == 'completed']
        if not completed:
            tk.Label(completed_wrap, text="No completed rides yet.", bg="#f7f7f7",
                     fg="#666").pack(pady=24)
        else:
            for r in completed:
                self.ride_card(completed_wrap, r, actions=[])

    # rider action helpers that also refresh
    def complete_ride_rider(self, ride_id):
        success, message = self.ride_manager.complete_ride(ride_id, self.current_user.email)
        if success:
            self.show_success(message)
            self.refresh_rider_tabs()
        else:
            self.show_error(message)

    # =============================
    # Driver Dashboard
    # =============================
    def build_driver_tabs(self):
        self.clear_widgets(self.content_frame)

        title = ttk.Label(self.content_frame, text="Driver Dashboard", style="Title.TLabel")
        title.pack(pady=(0, 8))

        # If driver has no vehicle, show registration form only
        if not getattr(self.current_user, 'vehicle', None):
            self._build_vehicle_registration(self.content_frame)
            return

        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Tabs
        self.tab_available = tk.Frame(self.notebook, bg="#f7f7f7")
        self.tab_ongoing = tk.Frame(self.notebook, bg="#f7f7f7")
        self.tab_canceled = tk.Frame(self.notebook, bg="#f7f7f7")

        self.notebook.add(self.tab_available, text="Available Rides")
        self.notebook.add(self.tab_ongoing, text="Ongoing Rides")
        self.notebook.add(self.tab_canceled, text="Canceled Rides")

        self.refresh_driver_tabs()

    def _build_vehicle_registration(self, parent):
        container = tk.Frame(parent, bg="#f7f7f7")
        container.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        ttk.Label(container, text="Vehicle Registration", style="Section.TLabel").pack(anchor='w', pady=(0, 8))

        row1, self.plate_entry = self.create_entry_field("License Plate Number", container)
        row1.pack(fill=tk.X, pady=6)
        row2, self.type_entry = self.create_entry_field("Vehicle Type (e.g., Sedan, SUV)", container)
        row2.pack(fill=tk.X, pady=6)
        row3, self.model_entry = self.create_entry_field("Vehicle Model", container)
        row3.pack(fill=tk.X, pady=6)

        btn = tk.Button(container, text="Register Vehicle", bg="#198754", fg="white",
                        relief=tk.FLAT, padx=12, pady=8, command=self.register_vehicle)
        btn.pack(anchor='e', pady=(8, 0))

    def refresh_driver_tabs(self):
        # update status chip
        self.update_driver_status()

        # Available
        for w in self.tab_available.winfo_children():
            w.destroy()
        avail_wrap = self.make_scrollable(self.tab_available)

        available = self.ride_manager.get_available_rides()
        if not available:
            tk.Label(avail_wrap, text="No rides available at the moment.", bg="#f7f7f7",
                     fg="#666").pack(pady=24)
        else:
            for r in available:
                actions = []
                actions.append((
                    "Accept Ride",
                    lambda rid=r.ride_id: self.accept_ride_driver(rid),
                    {"bg": "#198754"}
                ))
                self.ride_card(avail_wrap, r, actions)

        # Ongoing
        for w in self.tab_ongoing.winfo_children():
            w.destroy()
        ongoing_wrap = self.make_scrollable(self.tab_ongoing)

        try:
            rides = self.ride_manager.get_user_rides(self.current_user.email)
            ongoing_rides = [
                r for r in rides
                if getattr(r, 'status', '') in ("accepted", "ongoing", "started")
                and getattr(r, 'driver_email', None) == self.current_user.email
            ]
        except Exception:
            ongoing_rides = []

        if not ongoing_rides:
            tk.Label(ongoing_wrap, text="No ongoing rides.", bg="#f7f7f7", fg="#666").pack(pady=24)
        else:
            for r in ongoing_rides:
                actions = []
                if getattr(r, 'status', '') == 'accepted':
                    actions.append(("Start Ride", lambda rid=r.ride_id: self.start_ride_driver(rid), {"bg": "#0d6efd"}))
                if getattr(r, 'status', '') in ('ongoing', 'started'):
                    actions.append(("Complete Ride", lambda rid=r.ride_id: self.complete_ride_driver(rid), {"bg": "#198754"}))
                actions.append(("Cancel Ride", lambda rid=r.ride_id: self.cancel_ride_driver(rid), {"bg": "#dc3545"}))
                self.ride_card(ongoing_wrap, r, actions)

        # Canceled
        for w in self.tab_canceled.winfo_children():
            w.destroy()
        canceled_wrap = self.make_scrollable(self.tab_canceled)

        # We'll try to fetch canceled rides that have this driver or all with rider id, depending on backend capabilities.
        # If RideManager exposes a dedicated method, swap here; otherwise, show a generic message.
        try:
            # Heuristic: reuse user rides for rider list; for drivers, RideManager may expose get_canceled_rides.
            canceled = []
            if hasattr(self.ride_manager, 'get_canceled_rides'):
                canceled = self.ride_manager.get_canceled_rides(driver_email=self.current_user.email)
        except Exception:
            canceled = []

        if not canceled:
            tk.Label(canceled_wrap, text="No canceled rides.", bg="#f7f7f7", fg="#666").pack(pady=24)
        else:
            for r in canceled:
                # Show rider id as requested if available
                rider_id = getattr(r, 'rider_email', getattr(r, 'user_email', 'N/A'))
                extra_parent = tk.Frame(canceled_wrap, bg="#f7f7f7")
                extra_parent.pack(fill=tk.X)
                self.ride_card(extra_parent, r, actions=[])
                tk.Label(extra_parent, text=f"Rider: {rider_id}", bg="#f7f7f7", fg="#555").pack(anchor='w', padx=16)

     # ---------------- Completed ----------------
        if not hasattr(self, 'tab_completed'):
            # Create tab once
            self.tab_completed = tk.Frame(self.notebook, bg="#f7f7f7")
            self.notebook.add(self.tab_completed, text="Completed Rides")

        for w in self.tab_completed.winfo_children():
            w.destroy()
        completed_wrap = self.make_scrollable(self.tab_completed)

        try:
            rides = self.ride_manager.get_user_rides(self.current_user.email)
            completed_rides = [
                r for r in rides
                if getattr(r, 'status', '') == "completed"
                and getattr(r, 'driver_email', None) == self.current_user.email
            ]
        except Exception:
            completed_rides = []

        if not completed_rides:
            tk.Label(completed_wrap, text="No completed rides yet.", bg="#f7f7f7", fg="#666").pack(pady=24)
        else:
            for r in completed_rides:
                extra_parent = tk.Frame(completed_wrap, bg="#f7f7f7")
                extra_parent.pack(fill=tk.X)
                self.ride_card(extra_parent, r, actions=[])
                rider_id = getattr(r, 'rider_email', getattr(r, 'user_email', 'N/A'))
                tk.Label(extra_parent, text=f"Rider: {rider_id}", bg="#f7f7f7", fg="#555").pack(anchor='w', padx=16)

    def update_driver_status(self):
        # Online if no current ride; Ongoing Ride if an accepted/ongoing ride exists
        status = "Online"
        try:
            rid = getattr(self.current_user, 'current_ride', None)
            if rid:
                r = self.ride_manager.get_ride_by_id(rid)
                if r and getattr(r, 'status', '') in ("accepted", "ongoing"):
                    status = "Ongoing Ride"
        except Exception:
            pass
        self.status_var.set(status)
        if hasattr(self, 'status_badge'):
            self.status_badge.configure(bg="#198754" if status != "Offline" else "#6c757d")

    # =============================
    # Actions (wire up refresh + constraints)
    # =============================
    def request_ride(self):
        pickup = self.pickup_entry.get().strip()
        drop = self.drop_entry.get().strip()
        if not pickup or not drop:
            self.show_error("Please enter pickup and drop locations")
            return
        success, ride_id, message = self.ride_manager.request_ride(self.current_user.email, pickup, drop)
        if success:
            self.show_success(f"Ride requested! Ride ID: {ride_id}")
            self.pickup_entry.delete(0, tk.END)
            self.drop_entry.delete(0, tk.END)
            self.refresh_rider_tabs()
            # switch to Requested tab for immediate feedback
            try:
                idx = self.notebook.tabs().index(self.notebook.select())  # ensure notebook exists
            except Exception:
                pass
            self.notebook.select(self.tab_requested)
        else:
            self.show_error(message)

    # Rider cancel (already in base)
    def cancel_ride(self, ride_id):
        success, message = self.ride_manager.cancel_ride(ride_id, self.current_user.email)
        if success:
            self.show_success(message)
            if hasattr(self.current_user, 'license_number'):
                self.refresh_driver_tabs()
            else:
                self.refresh_rider_tabs()
        else:
            self.show_error(message)

    # --- Driver actions enforcing single ongoing ride constraint ---
    def _has_ongoing(self):
        try:
            rid = getattr(self.current_user, 'current_ride', None)
            if not rid:
                return False
            r = self.ride_manager.get_ride_by_id(rid)
            return bool(r and getattr(r, 'status', '') in ("accepted", "ongoing"))
        except Exception:
            return False

    def accept_ride_driver(self, ride_id):
        # constraint: only if no ongoing ride
        if self._has_ongoing():
            messagebox.showwarning("Action blocked", "You already have an ongoing ride. Complete it before accepting a new one.")
            return
        success, message = self.ride_manager.accept_ride(ride_id, self.current_user.email)
        if success:
            self.current_user.current_ride = ride_id  # ✅ set ongoing ride
            self.show_success(message)
            self.refresh_driver_tabs()

        else:
            self.show_error(message)

    def start_ride_driver(self, ride_id):
        success, message = self.ride_manager.start_ride(ride_id, self.current_user.email)
        if success:
            self.current_user.current_ride = ride_id  # ✅ ensure current ride is tracked
            self.show_success(message)
            self.refresh_driver_tabs()
        else:
            self.show_error(message)

    def complete_ride_driver(self, ride_id):
        success, message = self.ride_manager.complete_ride(ride_id, self.current_user.email)
        if success:
            self.show_success(message)
            self.current_user.current_ride = None  # ✅ clear ongoing ride
            self.refresh_driver_tabs()

        else:
            self.show_error(message)

    def cancel_ride_driver(self, ride_id):
        success, message = self.ride_manager.cancel_ride(ride_id, self.current_user.email)
        if success:
            self.show_success(message)
            self.current_user.current_ride = None  # ✅ clear ongoing ride
            self.refresh_driver_tabs()

        else:
            self.show_error(message)

    # =============================
    # Vehicle Registration (driver)
    # =============================
    def register_vehicle(self):
        """Register vehicle for driver and rebuild driver tabs."""
        plate = self.plate_entry.get().strip()
        vehicle_type = self.type_entry.get().strip()
        model = self.model_entry.get().strip()

        if not all([plate, vehicle_type, model]):
            self.show_error("Please fill in all vehicle fields")
            return
        if not Validators.validate_vehicle_plate(plate):
            self.show_error("Please enter a valid license plate")
            return

        # Add to current_user
        self.current_user.add_vehicle(plate, vehicle_type, model)
        try:
            from db.connection import db_connection
            db = db_connection.get_database()
            db.users.update_one({"email": self.current_user.email}, {"$set": {"vehicle": self.current_user.vehicle}})
        except Exception:
            pass

        self.show_success("Vehicle registered successfully!")
        self.build_driver_tabs()

    # =============================
    # Periodic auto-refresh
    # =============================
    # def _auto_refresh(self):
    #     try:
    #         if hasattr(self.current_user, 'license_number'):
    #             self.refresh_driver_tabs()
    #         else:
    #             self.refresh_rider_tabs()
    #     finally:
    #         # re-arm timer
    #         self.root.after(self.AUTO_REFRESH_MS, self._auto_refresh)

    # =============================
    # BaseWindow overrides
    # =============================
    def logout(self):
        self.status_var.set("Offline")
        if hasattr(self, 'status_badge'):
            self.status_badge.configure(bg="#6c757d")
        self.auth_manager.logout_user()
        self.root.destroy()
        from gui.auth_windows import LoginWindow
        login_window = LoginWindow(self.auth_manager, show_welcome=False)
        login_window.run()

    def refresh_page(self):
        """Refresh current dashboard based on user type."""
        if hasattr(self.current_user, 'license_number'):
            self.refresh_driver_tabs()
        else:
            self.refresh_rider_tabs()

    def on_tab_changed(self, event):
        """Refresh page when switching tabs"""
        tab = event.widget.tab(event.widget.select(), "text")

        if hasattr(self.current_user, 'license_number'):
            # Driver dashboard
            self.refresh_driver_tabs()
        else:
            # Rider dashboard
            self.refresh_rider_tabs()