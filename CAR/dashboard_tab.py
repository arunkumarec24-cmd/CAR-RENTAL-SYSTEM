"""
dashboard_tab.py — Dashboard Tab for Car Rental System GUI.
Shows key statistics and recent rental activity.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from .theme import COLORS, FONTS, PAD
from .widgets import StatCard, CardFrame, make_treeview, refresh_tree


class DashboardTab(tk.Frame):
    """Main dashboard panel with live statistics and recent activity."""

    def __init__(self, parent, db_manager):
        super().__init__(parent, bg=COLORS["bg_primary"])
        self.db = db_manager
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # ── Header ───────────────────────────────────────────────────────
        header = tk.Frame(self, bg=COLORS["bg_primary"], pady=PAD["lg"])
        header.pack(fill="x", padx=PAD["xl"])

        tk.Label(
            header, text="Dashboard Overview",
            bg=COLORS["bg_primary"], fg=COLORS["text_primary"],
            font=FONTS["title"]
        ).pack(side="left")

        self.date_lbl = tk.Label(
            header, text="",
            bg=COLORS["bg_primary"], fg=COLORS["text_secondary"],
            font=FONTS["body"]
        )
        self.date_lbl.pack(side="right", pady=4)
        self._tick_clock()

        # ── Stats Grid ───────────────────────────────────────────────────
        stats_frame = tk.Frame(self, bg=COLORS["bg_primary"])
        stats_frame.pack(fill="x", padx=PAD["xl"], pady=(0, PAD["xl"]))

        for i in range(3):
            stats_frame.columnconfigure(i, weight=1)

        self.cards = {
            "available_cars": StatCard(stats_frame, "Available Cars", "🚗", COLORS["success"]),
            "rented_cars":    StatCard(stats_frame, "Rented Cars",    "🔑", COLORS["warning"]),
            "total_cars":     StatCard(stats_frame, "Total Fleet",    "🚙", COLORS["accent"]),
            "active_rentals": StatCard(stats_frame, "Active Rentals", "📅", COLORS["purple"]),
            "total_customers":StatCard(stats_frame, "Total Customers","👥", COLORS["teal"]),
            "total_revenue":  StatCard(stats_frame, "Total Revenue",  "💰", COLORS["gold"]),
        }

        # Grid placement (2 rows of 3)
        self.cards["available_cars"].grid( row=0, column=0, sticky="ew", padx=(0,PAD["md"]), pady=(0,PAD["md"]))
        self.cards["rented_cars"].grid(    row=0, column=1, sticky="ew", padx=PAD["md"],      pady=(0,PAD["md"]))
        self.cards["total_cars"].grid(     row=0, column=2, sticky="ew", padx=(PAD["md"],0),  pady=(0,PAD["md"]))
        self.cards["active_rentals"].grid( row=1, column=0, sticky="ew", padx=(0,PAD["md"]))
        self.cards["total_customers"].grid(row=1, column=1, sticky="ew", padx=PAD["md"])
        self.cards["total_revenue"].grid(  row=1, column=2, sticky="ew", padx=(PAD["md"],0))

        # ── Recent Rentals Table ─────────────────────────────────────────
        table_card = CardFrame(self, title="Recent Rental Activity")
        table_card.pack(fill="both", expand=True, padx=PAD["xl"], pady=(0, PAD["xl"]))

        cols = ("Rental ID", "Customer", "Car", "Start Date", "End Date", "Total (₹)", "Status")
        self.tree, t_frame = make_treeview(table_card, cols, heights=10)
        t_frame.pack(fill="both", expand=True, padx=PAD["md"], pady=PAD["md"])

        # Adjust column widths
        self.tree.column("Rental ID", width=80, anchor="center")
        self.tree.column("Total (₹)", width=100, anchor="e")
        self.tree.column("Status", width=100, anchor="center")

    def _tick_clock(self):
        now = datetime.now().strftime("%A, %d %B %Y  |  %I:%M:%S %p")
        self.date_lbl.config(text=now)
        self.after(1000, self._tick_clock)

    def refresh(self):
        """Update KPI numbers and fetch latest rentals."""
        stats = self.db.get_stats()
        for key, val in stats.items():
            if key in self.cards:
                display_val = f"₹{val:,.2f}" if key == "total_revenue" else str(val)
                self.cards[key].set_value(display_val)

        # Refresh table
        recent = self.db.get_recent_rentals(limit=15)
        # Format currency in the row before inserting
        formatted_rows = []
        for r in recent:
            row = list(r)
            row[5] = f"₹{row[5]:.2f}"  # index 5 is total_amount
            formatted_rows.append(row)

        refresh_tree(self.tree, formatted_rows)
