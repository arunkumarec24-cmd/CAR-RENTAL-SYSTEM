"""
rental_tab.py — Rental Management & Booking Tab.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import date
from .theme import COLORS, FONTS, PAD
from .widgets import (
    StyledButton, LabelEntry, LabelCombo, CardFrame,
    make_treeview, refresh_tree, make_search_bar
)
from .rental_logic import RentalLogic


class RentalManagementTab(tk.Frame):
    """Interface to issue new rentals and return cars."""

    def __init__(self, parent, db_manager):
        super().__init__(parent, bg=COLORS["bg_primary"])
        self.db = db_manager
        self.selected_rental_id = None
        
        # Caching for combobox IDs
        self._customer_map = {}
        self._car_map = {}

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=COLORS["bg_primary"], pady=PAD["lg"])
        hdr.pack(fill="x", padx=PAD["xl"])

        tk.Label(
            hdr, text="Rentals & Returns",
            bg=COLORS["bg_primary"], fg=COLORS["text_primary"],
            font=FONTS["title"]
        ).pack(side="left")

        search_frame, self.search_var = make_search_bar(hdr, self.search, "Search rentals...")
        search_frame.pack(side="right")

        main_body = tk.Frame(self, bg=COLORS["bg_primary"])
        main_body.pack(fill="both", expand=True, padx=PAD["xl"], pady=(0, PAD["xl"]))

        # -- Left Panel: Issue Rental Form --
        form_card = CardFrame(main_body, title="New Booking")
        form_card.pack(side="left", fill="y", padx=(0, PAD["lg"]))

        form_inner = tk.Frame(form_card, bg=COLORS["bg_secondary"], padx=PAD["lg"], pady=PAD["md"])
        form_inner.pack(fill="both", expand=True)

        self.inputs = {
            "customer": LabelCombo(form_inner, "Select Customer", width=30),
            "car":      LabelCombo(form_inner, "Select Available Car", width=30),
            "start":    LabelEntry(form_inner, "Start Date (YYYY-MM-DD)", width=32),
            "end":      LabelEntry(form_inner, "End Date (YYYY-MM-DD)", width=32),
        }

        for w in self.inputs.values():
            w.pack(fill="x", pady=(0, PAD["md"]))
            
        # Defaults
        self.inputs["start"].set(date.today().strftime("%Y-%m-%d"))

        btn_frame = tk.Frame(form_inner, bg=COLORS["bg_secondary"], pady=PAD["md"])
        btn_frame.pack(fill="x", side="bottom")

        StyledButton(btn_frame, "✅ Calculate & Book", command=self.book_rental, style="success", width=20).pack(fill="x", pady=(0, PAD["sm"]))
        StyledButton(btn_frame, "🧹 Clear Form", command=self.clear_form, style="neutral", width=20).pack(fill="x")

        # -- Right Panel: Active & Past Rentals Table --
        table_card = CardFrame(main_body)
        table_card.pack(side="right", fill="both", expand=True)

        tb = tk.Frame(table_card, bg=COLORS["bg_secondary"], padx=PAD["md"], pady=PAD["sm"])
        tb.pack(fill="x")
        
        tk.Label(tb, text="Rental Log", bg=COLORS["bg_secondary"], fg=COLORS["text_primary"], font=FONTS["subheading"]).pack(side="left")
        
        StyledButton(tb, "⬇️ Export CSV", command=self.export_csv, style="neutral", pady=4).pack(side="right")
        StyledButton(tb, "🔄 Refresh", command=self.refresh, style="neutral", pady=4).pack(side="right", padx=PAD["sm"])
        
        # Action buttons for selected rows
        self.btn_return = StyledButton(tb, "🔙 Return Car", command=self.return_car, style="warning", pady=4)
        self.btn_return.pack(side="right", padx=PAD["sm"])
        
        self.btn_receipt = StyledButton(tb, "📄 View Receipt", command=self.view_receipt, style="primary", pady=4)
        self.btn_receipt.pack(side="right", padx=PAD["sm"])

        cols = ("Rental ID", "Customer", "Car", "Start", "End", "Amount (₹)", "Status", "Date Booked")
        self.tree, t_frame = make_treeview(table_card, cols)
        t_frame.pack(fill="both", expand=True, padx=PAD["md"], pady=(0, PAD["md"]))

        self.tree.column("Rental ID", width=60, anchor="center")
        self.tree.column("Amount (₹)", width=90, anchor="e")
        self.tree.column("Status", width=90, anchor="center")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # ─────────────────────────────────────────────────────────────────────────

    def populate_dropdowns(self):
        # Customers
        custs = self.db.get_all_customers()
        self._customer_map = {f"{c['name']} (ID: {c['customer_id']})": c['customer_id'] for c in custs}
        self.inputs["customer"].set_values(list(self._customer_map.keys()))

        # Available Cars
        cars = self.db.get_available_cars()
        self._car_map = {f"{c['brand']} {c['model']} (ID: {c['car_id']}) - ₹{c['price_per_day']}/day": c['car_id'] for c in cars}
        self.inputs["car"].set_values(list(self._car_map.keys()))

    def clear_form(self):
        self.inputs["customer"].clear()
        self.inputs["car"].clear()
        self.inputs["start"].set(date.today().strftime("%Y-%m-%d"))
        self.inputs["end"].clear()

    def refresh(self):
        self.selected_rental_id = None
        self.tree.selection_remove(self.tree.selection())
        self.populate_dropdowns()
        
        rows = self.db.get_all_rentals()
        self._populate_tree(rows)

    def search(self):
        q = self.search_var.get().strip()
        if not q or q.startswith("Search"):
            self.refresh()
            return
        rows = self.db.search_rentals(q)
        self._populate_tree(rows)

    def _populate_tree(self, rows):
        fmt = []
        for r in rows:
            lst = list(r)
            lst[5] = f"₹{lst[5]:.2f}"
            fmt.append(lst)
        refresh_tree(self.tree, fmt)

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            self.selected_rental_id = None
            return
        item = self.tree.item(sel[0])["values"]
        self.selected_rental_id = item[0]

    def book_rental(self):
        c_str = self.inputs["customer"].get()
        v_str = self.inputs["car"].get()
        start = self.inputs["start"].get()
        end   = self.inputs["end"].get()

        if not c_str or not v_str:
            messagebox.showwarning("Missing Info", "Please select a customer and a car.")
            return

        err = RentalLogic.validate_rental_dates(start, end)
        if err:
            messagebox.showerror("Date Error", err)
            return

        cust_id = self._customer_map.get(c_str)
        car_id  = self._car_map.get(v_str)
        if not cust_id or not car_id:
            messagebox.showerror("Error", "Invalid selection.")
            return

        # Calculate cost
        car_data = self.db.get_car_by_id(car_id)
        days = RentalLogic.calculate_rental_days(start, end)
        total = RentalLogic.calculate_total_cost(car_data["price_per_day"], days)

        msg = f"Duration: {days} days\nRate: ₹{car_data['price_per_day']}/day\n\nTotal Cost: ₹{total:.2f}\n\nProceed with booking?"
        if not messagebox.askyesno("Confirm Booking", msg):
            return

        try:
            rental_id = self.db.add_rental(cust_id, car_id, start, end, total)
            self.db.set_car_status(car_id, "Rented")
            
            messagebox.showinfo("Success", f"Booking confirmed! Rental ID: {rental_id}")
            self.refresh()
            self.clear_form()
            
            # Auto-generate receipt
            self._generate_and_save_receipt(rental_id, show_info=False)
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Booking failed: {e}")

    def return_car(self):
        if not self.selected_rental_id:
            messagebox.showwarning("Selection Required", "Please select a rental to return.")
            return
            
        rental = self.db.get_rental_by_id(self.selected_rental_id)
        if rental["status"] == "Returned":
            messagebox.showinfo("Info", "This rental has already been returned.")
            return
            
        if messagebox.askyesno("Confirm Return", f"Process return for Rental #{self.selected_rental_id}?"):
            try:
                self.db.return_car(self.selected_rental_id)
                messagebox.showinfo("Success", "Car returned successfully! It is now available.")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Database Error", f"Return failed: {e}")

    def view_receipt(self):
        if not self.selected_rental_id:
            messagebox.showwarning("Selection Required", "Please select a rental to view receipt.")
            return
        self._generate_and_save_receipt(self.selected_rental_id, show_info=True)
            
    def _generate_and_save_receipt(self, rental_id, show_info=True):
        data = self.db.get_rental_by_id(rental_id)
        if not data:
            return
            
        days = RentalLogic.calculate_rental_days(data["start_date"], data["end_date"])
        
        receipt_dict = dict(data)
        receipt_dict["customer_name"] = data["customer_name"]
        receipt_dict["days"] = days
        
        text = RentalLogic.generate_receipt(receipt_dict)
        path = RentalLogic.save_receipt(text, rental_id)
        
        if show_info:
            # Show a custom popup with the text
            top = tk.Toplevel(self)
            top.title(f"Receipt - Rental #{rental_id}")
            top.geometry("500x600")
            top.configure(bg=COLORS["bg_primary"])
            
            txt = tk.Text(top, bg=COLORS["bg_tertiary"], fg=COLORS["text_primary"], 
                          font=FONTS["mono"], padx=20, pady=20)
            txt.pack(fill="both", expand=True, padx=PAD["md"], pady=PAD["md"])
            txt.insert("1.0", text)
            txt.config(state="disabled")
            
            lbl = tk.Label(top, text=f"Saved to: {path}", bg=COLORS["bg_primary"], fg=COLORS["text_secondary"])
            lbl.pack(pady=(0, PAD["md"]))

    def export_csv(self):
        try:
            path = RentalLogic.export_rentals_to_csv(self.db.get_all_rentals())
            messagebox.showinfo("Export Successful", f"Exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))
