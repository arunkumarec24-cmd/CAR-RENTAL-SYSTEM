"""
car_tab.py — Car Management Tab (CRUD).
"""

import tkinter as tk
from tkinter import messagebox
from .theme import COLORS, FONTS, PAD
from .widgets import (
    StyledButton, LabelEntry, LabelCombo, CardFrame,
    make_treeview, refresh_tree, make_search_bar
)
from .rental_logic import RentalLogic


class CarManagementTab(tk.Frame):
    """Full CRUD interface for fleet management."""

    STATUSES = ["Available", "Rented", "Maintenance"]

    def __init__(self, parent, db_manager):
        super().__init__(parent, bg=COLORS["bg_primary"])
        self.db = db_manager
        self.selected_id = None

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # ── Header & Search ──────────────────────────────────────────────
        hdr = tk.Frame(self, bg=COLORS["bg_primary"], pady=PAD["lg"])
        hdr.pack(fill="x", padx=PAD["xl"])

        tk.Label(
            hdr, text="Car Management",
            bg=COLORS["bg_primary"], fg=COLORS["text_primary"],
            font=FONTS["title"]
        ).pack(side="left")

        search_frame, self.search_var = make_search_bar(hdr, self.search, "Search by brand, model, plate...")
        search_frame.pack(side="right")

        # ── Split Layout: Form (Left) | Table (Right) ────────────────────
        main_body = tk.Frame(self, bg=COLORS["bg_primary"])
        main_body.pack(fill="both", expand=True, padx=PAD["xl"], pady=(0, PAD["xl"]))

        # -- Left Form --
        form_card = CardFrame(main_body, title="Car Details")
        form_card.pack(side="left", fill="y", padx=(0, PAD["lg"]))

        form_inner = tk.Frame(form_card, bg=COLORS["bg_secondary"], padx=PAD["lg"], pady=PAD["md"])
        form_inner.pack(fill="both", expand=True)

        self.inputs = {
            "brand":  LabelEntry(form_inner, "Brand (e.g., Toyota)"),
            "model":  LabelEntry(form_inner, "Model (e.g., Camry)"),
            "year":   LabelEntry(form_inner, "Year"),
            "price":  LabelEntry(form_inner, "Price per Day (₹)"),
            "color":  LabelEntry(form_inner, "Color"),
            "plate":  LabelEntry(form_inner, "Plate Number"),
            "status": LabelCombo(form_inner, "Status", self.STATUSES),
        }

        for i, (k, widget) in enumerate(self.inputs.items()):
            widget.pack(fill="x", pady=(0, PAD["md"]))
        self.inputs["status"].set("Available")

        # Buttons
        btn_frame = tk.Frame(form_inner, bg=COLORS["bg_secondary"], pady=PAD["sm"])
        btn_frame.pack(fill="x", side="bottom")

        row1 = tk.Frame(btn_frame, bg=COLORS["bg_secondary"])
        row1.pack(fill="x", pady=(0, PAD["xs"]))
        StyledButton(row1, "➕ Add", command=self.add_car, style="success").pack(side="left", expand=True, fill="x", padx=(0, 2))
        StyledButton(row1, "💾 Update", command=self.update_car, style="primary").pack(side="left", expand=True, fill="x", padx=(2, 0))

        row2 = tk.Frame(btn_frame, bg=COLORS["bg_secondary"])
        row2.pack(fill="x")
        StyledButton(row2, "🧹 Clear", command=self.clear_form, style="neutral").pack(side="left", expand=True, fill="x", padx=(0, 2))
        StyledButton(row2, "🗑️ Delete", command=self.delete_car, style="danger").pack(side="left", expand=True, fill="x", padx=(2, 0))

        # -- Right Table --
        table_card = CardFrame(main_body)
        table_card.pack(side="right", fill="both", expand=True)

        # Top Toolbar for table
        tb = tk.Frame(table_card, bg=COLORS["bg_secondary"], padx=PAD["md"], pady=PAD["sm"])
        tb.pack(fill="x")
        tk.Label(tb, text="Fleet Roster", bg=COLORS["bg_secondary"], fg=COLORS["text_primary"], font=FONTS["subheading"]).pack(side="left")
        StyledButton(tb, "⬇️ Export CSV", command=self.export_csv, style="neutral", pady=4).pack(side="right")
        StyledButton(tb, "🔄 Refresh", command=self.refresh, style="neutral", pady=4).pack(side="right", padx=PAD["sm"])

        cols = ("ID", "Brand", "Model", "Year", "Price/Day", "Status", "Color", "Plate No.")
        self.tree, t_frame = make_treeview(table_card, cols)
        t_frame.pack(fill="both", expand=True, padx=PAD["md"], pady=(0, PAD["md"]))

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Year", width=60, anchor="center")
        self.tree.column("Price/Day", width=80, anchor="e")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # ─────────────────────────────────────────────────────────────────────────

    def get_form_data(self):
        return {
            "brand": self.inputs["brand"].get(),
            "model": self.inputs["model"].get(),
            "year": self.inputs["year"].get(),
            "price": self.inputs["price"].get(),
            "status": self.inputs["status"].get(),
            "color": self.inputs["color"].get(),
            "plate": self.inputs["plate"].get(),
        }

    def clear_form(self):
        self.selected_id = None
        for k, w in self.inputs.items():
            if k == "status":
                w.set("Available")
            else:
                w.clear()
        self.tree.selection_remove(self.tree.selection())

    def refresh(self):
        self.clear_form()
        rows = self.db.get_all_cars()
        self._populate_tree(rows)

    def search(self):
        q = self.search_var.get().strip()
        if not q or q.startswith("Search"):
            self.refresh()
            return
        rows = self.db.search_cars(q)
        self._populate_tree(rows)

    def _populate_tree(self, rows):
        fmt_rows = []
        for r in rows:
            lst = list(r)
            lst[4] = f"₹{lst[4]:.2f}"  # format price
            fmt_rows.append(lst)
        refresh_tree(self.tree, fmt_rows)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])["values"]
        self.selected_id = item[0]

        self.inputs["brand"].set(item[1])
        self.inputs["model"].set(item[2])
        self.inputs["year"].set(item[3])
        self.inputs["price"].set(str(item[4]).replace("₹", "").replace(",", ""))
        self.inputs["status"].set(item[5])
        self.inputs["color"].set(item[6])
        self.inputs["plate"].set(item[7])

    def add_car(self):
        d = self.get_form_data()
        err = RentalLogic.validate_car(d["brand"], d["model"], d["year"], d["price"], d["plate"])
        if err:
            messagebox.showerror("Validation Error", err)
            return

        try:
            self.db.add_car(
                d["brand"], d["model"], int(d["year"]),
                float(d["price"]), d["status"], d["color"], d["plate"]
            )
            messagebox.showinfo("Success", "Car added successfully.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add car: {e}")

    def update_car(self):
        if not self.selected_id:
            messagebox.showwarning("Selection Required", "Please select a car from the table to update.")
            return

        d = self.get_form_data()
        err = RentalLogic.validate_car(d["brand"], d["model"], d["year"], d["price"], d["plate"])
        if err:
            messagebox.showerror("Validation Error", err)
            return

        try:
            self.db.update_car(
                self.selected_id, d["brand"], d["model"], int(d["year"]),
                float(d["price"]), d["status"], d["color"], d["plate"]
            )
            messagebox.showinfo("Success", "Car updated successfully.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update car: {e}")

    def delete_car(self):
        if not self.selected_id:
            messagebox.showwarning("Selection Required", "Please select a car to delete.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete car ID {self.selected_id}?"):
            try:
                self.db.delete_car(self.selected_id)
                messagebox.showinfo("Success", "Car deleted.")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Database Error", f"Cannot delete car (might be referenced in rentals): {e}")

    def export_csv(self):
        try:
            path = RentalLogic.export_cars_to_csv(self.db.get_all_cars())
            messagebox.showinfo("Export Successful", f"Exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))
