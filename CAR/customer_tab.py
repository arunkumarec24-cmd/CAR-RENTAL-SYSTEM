"""
customer_tab.py — Customer Management Tab (CRUD).
"""

import tkinter as tk
from tkinter import messagebox
from .theme import COLORS, FONTS, PAD
from .widgets import (
    StyledButton, LabelEntry, CardFrame,
    make_treeview, refresh_tree, make_search_bar
)
from .rental_logic import RentalLogic


class CustomerManagementTab(tk.Frame):
    """Full CRUD interface for customer management."""

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
            hdr, text="Customer Directory",
            bg=COLORS["bg_primary"], fg=COLORS["text_primary"],
            font=FONTS["title"]
        ).pack(side="left")

        search_frame, self.search_var = make_search_bar(hdr, self.search, "Search name, phone, license...")
        search_frame.pack(side="right")

        # ── Split Layout: Form (Left) | Table (Right) ────────────────────
        main_body = tk.Frame(self, bg=COLORS["bg_primary"])
        main_body.pack(fill="both", expand=True, padx=PAD["xl"], pady=(0, PAD["xl"]))

        # -- Left Form --
        form_card = CardFrame(main_body, title="Customer Details")
        form_card.pack(side="left", fill="y", padx=(0, PAD["lg"]))

        form_inner = tk.Frame(form_card, bg=COLORS["bg_secondary"], padx=PAD["lg"], pady=PAD["md"])
        form_inner.pack(fill="both", expand=True)

        self.inputs = {
            "name":    LabelEntry(form_inner, "Full Name"),
            "phone":   LabelEntry(form_inner, "Phone Number"),
            "email":   LabelEntry(form_inner, "Email Address"),
            "license": LabelEntry(form_inner, "Driving License Number"),
            "address": LabelEntry(form_inner, "Home Address"),
        }

        for w in self.inputs.values():
            w.pack(fill="x", pady=(0, PAD["md"]))

        # Buttons
        btn_frame = tk.Frame(form_inner, bg=COLORS["bg_secondary"], pady=PAD["sm"])
        btn_frame.pack(fill="x", side="bottom")

        row1 = tk.Frame(btn_frame, bg=COLORS["bg_secondary"])
        row1.pack(fill="x", pady=(0, PAD["xs"]))
        StyledButton(row1, "➕ Add", command=self.add_customer, style="success").pack(side="left", expand=True, fill="x", padx=(0, 2))
        StyledButton(row1, "💾 Update", command=self.update_customer, style="primary").pack(side="left", expand=True, fill="x", padx=(2, 0))

        row2 = tk.Frame(btn_frame, bg=COLORS["bg_secondary"])
        row2.pack(fill="x")
        StyledButton(row2, "🧹 Clear", command=self.clear_form, style="neutral").pack(side="left", expand=True, fill="x", padx=(0, 2))
        StyledButton(row2, "🗑️ Delete", command=self.delete_customer, style="danger").pack(side="left", expand=True, fill="x", padx=(2, 0))

        # -- Right Table --
        table_card = CardFrame(main_body)
        table_card.pack(side="right", fill="both", expand=True)

        tb = tk.Frame(table_card, bg=COLORS["bg_secondary"], padx=PAD["md"], pady=PAD["sm"])
        tb.pack(fill="x")
        tk.Label(tb, text="Registered Customers", bg=COLORS["bg_secondary"], fg=COLORS["text_primary"], font=FONTS["subheading"]).pack(side="left")
        StyledButton(tb, "⬇️ Export CSV", command=self.export_csv, style="neutral", pady=4).pack(side="right")
        StyledButton(tb, "🔄 Refresh", command=self.refresh, style="neutral", pady=4).pack(side="right", padx=PAD["sm"])

        cols = ("ID", "Name", "Phone", "Email", "License No.", "Address")
        self.tree, t_frame = make_treeview(table_card, cols)
        t_frame.pack(fill="both", expand=True, padx=PAD["md"], pady=(0, PAD["md"]))

        self.tree.column("ID", width=50, anchor="center")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # ─────────────────────────────────────────────────────────────────────────

    def get_form_data(self):
        return {k: v.get() for k, v in self.inputs.items()}

    def clear_form(self):
        self.selected_id = None
        for w in self.inputs.values():
            w.clear()
        self.tree.selection_remove(self.tree.selection())

    def refresh(self):
        self.clear_form()
        rows = self.db.get_all_customers()
        refresh_tree(self.tree, rows)

    def search(self):
        q = self.search_var.get().strip()
        if not q or q.startswith("Search"):
            self.refresh()
            return
        rows = self.db.search_customers(q)
        refresh_tree(self.tree, rows)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])["values"]
        self.selected_id = item[0]

        self.inputs["name"].set(item[1])
        self.inputs["phone"].set(item[2])
        self.inputs["email"].set(item[3] if item[3] != "None" else "")
        self.inputs["license"].set(item[4])
        self.inputs["address"].set(item[5] if item[5] != "None" else "")

    def add_customer(self):
        d = self.get_form_data()
        err = RentalLogic.validate_customer(d["name"], d["phone"], d["license"])
        if err:
            messagebox.showerror("Validation Error", err)
            return

        try:
            self.db.add_customer(d["name"], d["phone"], d["email"], d["license"], d["address"])
            messagebox.showinfo("Success", "Customer added successfully.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add customer: {e}")

    def update_customer(self):
        if not self.selected_id:
            messagebox.showwarning("Selection Required", "Please select a customer to update.")
            return

        d = self.get_form_data()
        err = RentalLogic.validate_customer(d["name"], d["phone"], d["license"])
        if err:
            messagebox.showerror("Validation Error", err)
            return

        try:
            self.db.update_customer(self.selected_id, d["name"], d["phone"], d["email"], d["license"], d["address"])
            messagebox.showinfo("Success", "Customer updated successfully.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update customer: {e}")

    def delete_customer(self):
        if not self.selected_id:
            messagebox.showwarning("Selection Required", "Please select a customer to delete.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete customer ID {self.selected_id}?"):
            try:
                self.db.delete_customer(self.selected_id)
                messagebox.showinfo("Success", "Customer deleted.")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Database Error", f"Cannot delete customer (might be referenced in rentals): {e}")

    def export_csv(self):
        try:
            path = RentalLogic.export_customers_to_csv(self.db.get_all_customers())
            messagebox.showinfo("Export Successful", f"Exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))
