"""
rental_logic.py — Business logic layer for Car Rental System.

Responsibilities:
  - Rental cost calculation
  - Input validation
  - Receipt / invoice generation (returns formatted string)
  - CSV export helpers
"""

import csv
import os
from datetime import datetime, date

# Exports folder (sibling of the package directory)
EXPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
os.makedirs(EXPORTS_DIR, exist_ok=True)


class RentalLogic:
    """Core business logic: cost calculation, validation, receipt & CSV export."""

    # ──────────────────────────── DATE / COST ────────────────────────────────

    @staticmethod
    def calculate_rental_days(start_date_str: str, end_date_str: str) -> int:
        """Return the number of rental days (minimum 1)."""
        fmt = "%Y-%m-%d"
        try:
            start = datetime.strptime(start_date_str, fmt).date()
            end   = datetime.strptime(end_date_str,   fmt).date()
            delta = (end - start).days
            return max(delta, 1)
        except ValueError:
            raise ValueError("Dates must be in YYYY-MM-DD format.")

    @staticmethod
    def calculate_total_cost(price_per_day: float, days: int) -> float:
        """Return total rental cost (price_per_day × days)."""
        return round(price_per_day * days, 2)

    @staticmethod
    def validate_rental_dates(start_date_str: str, end_date_str: str) -> str | None:
        """
        Return an error message string if dates are invalid, else None.
        Checks: format, end >= start, start >= today.
        """
        fmt = "%Y-%m-%d"
        try:
            start = datetime.strptime(start_date_str, fmt).date()
            end   = datetime.strptime(end_date_str,   fmt).date()
        except ValueError:
            return "Dates must be in YYYY-MM-DD format."

        if start < date.today():
            return "Start date cannot be in the past."
        if end < start:
            return "End date must be on or after start date."
        return None

    # ──────────────────────────── VALIDATION ─────────────────────────────────

    @staticmethod
    def validate_car(brand, model, year_str, price_str, plate_number):
        """Validate car form fields. Returns error string or None."""
        if not brand.strip():
            return "Brand is required."
        if not model.strip():
            return "Model is required."
        try:
            year = int(year_str)
            if year < 1990 or year > date.today().year + 1:
                return f"Year must be between 1990 and {date.today().year + 1}."
        except ValueError:
            return "Year must be a valid integer."
        try:
            price = float(price_str)
            if price <= 0:
                return "Price per day must be positive."
        except ValueError:
            return "Price per day must be a valid number."
        if not plate_number.strip():
            return "Plate number is required."
        return None

    @staticmethod
    def validate_customer(name, phone, license_number):
        """Validate customer form fields. Returns error string or None."""
        if not name.strip():
            return "Customer name is required."
        if not phone.strip():
            return "Phone number is required."
        if not license_number.strip():
            return "Driving license number is required."
        return None

    # ──────────────────────────── RECEIPT ────────────────────────────────────

    @staticmethod
    def generate_receipt(rental_data: dict) -> str:
        """
        Generate a formatted text receipt.

        rental_data keys:
          rental_id, customer_name, phone, email, license_number,
          brand, model, year, plate_number,
          start_date, end_date, days, price_per_day, total_amount, status
        """
        sep  = "═" * 52
        sep2 = "─" * 52
        now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            sep,
            "       🚗  CAR RENTAL SYSTEM — RECEIPT  🚗",
            sep,
            f"  Receipt Date   : {now}",
            f"  Rental ID      : #{rental_data.get('rental_id', 'N/A')}",
            sep2,
            "  CUSTOMER INFORMATION",
            sep2,
            f"  Name           : {rental_data.get('customer_name', '')}",
            f"  Phone          : {rental_data.get('phone', '')}",
            f"  Email          : {rental_data.get('email', '') or 'N/A'}",
            f"  License No.    : {rental_data.get('license_number', '')}",
            sep2,
            "  VEHICLE INFORMATION",
            sep2,
            f"  Car            : {rental_data.get('brand', '')} {rental_data.get('model', '')} ({rental_data.get('year', '')})",
            f"  Plate No.      : {rental_data.get('plate_number', '')}",
            sep2,
            "  RENTAL DETAILS",
            sep2,
            f"  Start Date     : {rental_data.get('start_date', '')}",
            f"  End Date       : {rental_data.get('end_date', '')}",
            f"  Duration       : {rental_data.get('days', '')} day(s)",
            f"  Rate / Day     : ₹{rental_data.get('price_per_day', 0):.2f}",
            sep2,
            f"  TOTAL AMOUNT   : ₹{rental_data.get('total_amount', 0):.2f}",
            f"  Status         : {rental_data.get('status', 'Active')}",
            sep,
            "   Thank you for choosing Car Rental System!",
            sep,
        ]
        return "\n".join(lines)

    @staticmethod
    def save_receipt(receipt_text: str, rental_id: int) -> str:
        """Save receipt to exports/ and return the file path."""
        filename = f"receipt_rental_{rental_id}.txt"
        path = os.path.join(EXPORTS_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(receipt_text)
        return path

    # ──────────────────────────── CSV EXPORT ─────────────────────────────────

    @staticmethod
    def export_cars_to_csv(rows) -> str:
        """Export car records to CSV and return the file path."""
        path = os.path.join(EXPORTS_DIR, f"cars_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        headers = ["Car ID", "Brand", "Model", "Year", "Price/Day", "Status", "Color", "Plate No."]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(list(row))
        return path

    @staticmethod
    def export_customers_to_csv(rows) -> str:
        """Export customer records to CSV and return the file path."""
        path = os.path.join(EXPORTS_DIR, f"customers_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        headers = ["Customer ID", "Name", "Phone", "Email", "License No.", "Address"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(list(row))
        return path

    @staticmethod
    def export_rentals_to_csv(rows) -> str:
        """Export rental records to CSV and return the file path."""
        path = os.path.join(EXPORTS_DIR, f"rentals_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        headers = ["Rental ID", "Customer", "Car", "Start Date", "End Date", "Total (₹)", "Status", "Created At"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(list(row))
        return path
