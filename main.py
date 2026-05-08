"""
main.py — Main Application Entry Point
"""

import tkinter as tk
from tkinter import ttk
import os

from CAR.theme import COLORS, FONTS, PAD, apply_treeview_style
from CAR.db_manager import DatabaseManager
from CAR.login_window import LoginWindow
from CAR.dashboard_tab import DashboardTab
from CAR.car_tab import CarManagementTab
from CAR.customer_tab import CustomerManagementTab
from CAR.rental_tab import RentalManagementTab


class Application:
    """Main Application Window (Post-Login)."""

    def __init__(self, db_manager):
        self.db = db_manager
        
        self.root = tk.Tk()
        self.root.title("Car Rental System - Admin Panel")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=COLORS["bg_primary"])

        self._center_window(1200, 800)
        self._setup_styles()
        self._build_ui()

    def _center_window(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _setup_styles(self):
        style = ttk.Style()
        apply_treeview_style(style)

        # Notebook (Tabs) styling
        style.configure(
            "Dark.TNotebook",
            background=COLORS["bg_primary"],
            borderwidth=0,
            padding=0
        )
        style.configure(
            "Dark.TNotebook.Tab",
            background=COLORS["bg_secondary"],
            foreground=COLORS["text_primary"],
            padding=(PAD["xl"], PAD["md"]),
            font=FONTS["heading"],
            borderwidth=0
        )
        style.map(
            "Dark.TNotebook.Tab",
            background=[("selected", COLORS["accent"])],
            foreground=[("selected", COLORS["text_primary"])]
        )

    def _build_ui(self):
        # Top banner
        banner = tk.Frame(self.root, bg=COLORS["bg_tertiary"], height=60)
        banner.pack(fill="x", side="top")
        banner.pack_propagate(False)

        tk.Label(
            banner, text="🚗  CAR RENTAL SYSTEM",
            bg=COLORS["bg_tertiary"], fg=COLORS["accent"],
            font=FONTS["title"]
        ).pack(side="left", padx=PAD["xl"])

        logout_btn = tk.Button(
            banner, text="Logout",
            bg=COLORS["danger"], fg=COLORS["text_primary"],
            activebackground=COLORS["danger_hover"], activeforeground=COLORS["text_primary"],
            font=FONTS["button"], relief="flat", cursor="hand2",
            padx=20, command=self.logout
        )
        logout_btn.pack(side="right", padx=PAD["xl"], pady=12)

        # Tabs container
        self.notebook = ttk.Notebook(self.root, style="Dark.TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=PAD["md"], pady=PAD["md"])

        # Initialize tabs
        self.tab_dashboard = DashboardTab(self.notebook, self.db)
        self.tab_cars      = CarManagementTab(self.notebook, self.db)
        self.tab_customers = CustomerManagementTab(self.notebook, self.db)
        self.tab_rentals   = RentalManagementTab(self.notebook, self.db)

        # Add tabs
        self.notebook.add(self.tab_dashboard, text="📊 Dashboard")
        self.notebook.add(self.tab_cars,      text="🚙 Cars")
        self.notebook.add(self.tab_customers, text="👥 Customers")
        self.notebook.add(self.tab_rentals,   text="📅 Rentals")

        # Bind tab change event to refresh data
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _on_tab_change(self, event):
        """Refresh the currently selected tab."""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            self.tab_dashboard.refresh()
        elif current_tab == 1:
            self.tab_cars.refresh()
        elif current_tab == 2:
            self.tab_customers.refresh()
        elif current_tab == 3:
            self.tab_rentals.refresh()

    def logout(self):
        self.root.destroy()
        start_app()

    def run(self):
        self.root.mainloop()


def start_app():
    """Starts the application flow (Login -> Main App)."""
    db = DatabaseManager()
    
    # Use a hidden root for the login window to prevent ghost windows
    hidden_root = tk.Tk()
    hidden_root.withdraw()
    
    login_root = tk.Toplevel(hidden_root)
    
    def on_login_success():
        hidden_root.destroy()
        app = Application(db)
        app.run()

    # If login is closed by the 'X', destroy the hidden root too
    login_root.protocol("WM_DELETE_WINDOW", hidden_root.destroy)
    
    app = LoginWindow(login_root, db, on_login_success)
    hidden_root.mainloop()


if __name__ == "__main__":
    start_app()
