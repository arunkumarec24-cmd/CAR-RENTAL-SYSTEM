"""
login_window.py — Admin login screen for the Car Rental System.
"""

import tkinter as tk
from tkinter import messagebox
from .theme import COLORS, FONTS, PAD
from .widgets import StyledButton, LabelEntry


class LoginWindow:
    """Admin login screen built with Tkinter."""

    def __init__(self, root, db_manager, on_success):
        self.root = root
        self.db = db_manager
        self.on_success = on_success

        self.root.title("Car Rental System — Login")
        self.root.geometry("440x560")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg_primary"])

        self._center_window(440, 560)
        self._build_ui()

        # Bind Enter key to login
        self.root.bind("<Return>", lambda e: self.login())

    def _center_window(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # Outer wrapper to center vertically
        outer = tk.Frame(self.root, bg=COLORS["bg_primary"])
        outer.place(relx=0.5, rely=0.5, anchor="center")

        # Top Icon / Title
        tk.Label(
            outer, text="🚗",
            font=("Segoe UI Emoji", 48),
            bg=COLORS["bg_primary"], fg=COLORS["accent"]
        ).pack(pady=(0, 10))

        tk.Label(
            outer, text="Welcome Back",
            font=FONTS["login_title"],
            bg=COLORS["bg_primary"], fg=COLORS["text_primary"]
        ).pack()

        tk.Label(
            outer, text="Sign in to continue to Car Rental System",
            font=FONTS["body"],
            bg=COLORS["bg_primary"], fg=COLORS["text_secondary"]
        ).pack(pady=(5, 30))

        # Card container for inputs
        card = tk.Frame(
            outer,
            bg=COLORS["bg_secondary"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=30, pady=30
        )
        card.pack(fill="x")

        self.user_entry = LabelEntry(card, "Username", width=30)
        self.user_entry.pack(fill="x", pady=(0, 15))

        self.pass_entry = LabelEntry(card, "Password", show="•", width=30)
        self.pass_entry.pack(fill="x", pady=(0, 25))

        StyledButton(
            card, "Login",
            command=self.login,
            style="primary",
            width=30, pady=10
        ).pack(fill="x")

        # Focus first field
        self.user_entry.var.trace_add("write", lambda *args: None)
        self.root.after(100, lambda: self.user_entry.winfo_children()[1].focus())

    def login(self):
        usr = self.user_entry.get()
        pwd = self.pass_entry.get()

        if not usr or not pwd:
            messagebox.showwarning("Warning", "Please enter username and password.")
            return

        if self.db.verify_admin(usr, pwd):
            self.root.destroy()
            self.on_success()
        else:
            messagebox.showerror("Error", "Invalid username or password.")
            self.pass_entry.clear()
