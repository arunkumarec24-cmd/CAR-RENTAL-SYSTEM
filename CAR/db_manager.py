"""
db_manager.py — SQLite database manager for the Car Rental System.

Handles:
  - Auto-creation of tables (cars, customers, rentals, admins)
  - Full CRUD for every entity
  - Query helpers used by GUI tabs
"""

import sqlite3
import os
from datetime import datetime

# Place the DB one level up from this package folder
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "car_rental.db")


class DatabaseManager:
    """Central manager for all SQLite operations."""

    def __init__(self):
        self.db_path = DB_PATH
        self.initialize_database()

    # ──────────────────────────── CONNECTION ─────────────────────────────────

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # ──────────────────────────── SCHEMA INIT ────────────────────────────────

    def initialize_database(self):
        """Create tables if they don't already exist and seed admin account."""
        sql_statements = [
            # ── Admin users ──────────────────────────────────────────────
            """CREATE TABLE IF NOT EXISTS admins (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    NOT NULL UNIQUE,
                password TEXT    NOT NULL
            )""",

            # ── Cars ─────────────────────────────────────────────────────
            """CREATE TABLE IF NOT EXISTS cars (
                car_id       INTEGER PRIMARY KEY AUTOINCREMENT,
                brand        TEXT    NOT NULL,
                model        TEXT    NOT NULL,
                year         INTEGER NOT NULL,
                price_per_day REAL   NOT NULL,
                status       TEXT    NOT NULL DEFAULT 'Available',
                color        TEXT,
                plate_number TEXT UNIQUE
            )""",

            # ── Customers ─────────────────────────────────────────────────
            """CREATE TABLE IF NOT EXISTS customers (
                customer_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT NOT NULL,
                phone           TEXT NOT NULL,
                email           TEXT,
                license_number  TEXT NOT NULL UNIQUE,
                address         TEXT
            )""",

            # ── Rentals ───────────────────────────────────────────────────
            """CREATE TABLE IF NOT EXISTS rentals (
                rental_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id  INTEGER NOT NULL,
                car_id       INTEGER NOT NULL,
                start_date   TEXT    NOT NULL,
                end_date     TEXT    NOT NULL,
                total_amount REAL    NOT NULL DEFAULT 0,
                status       TEXT    NOT NULL DEFAULT 'Active',
                created_at   TEXT    NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (car_id)      REFERENCES cars(car_id)
            )""",
        ]

        with self.get_connection() as conn:
            for stmt in sql_statements:
                conn.execute(stmt)
            conn.commit()

            # Seed default admin if table is empty
            count = conn.execute("SELECT COUNT(*) FROM admins").fetchone()[0]
            if count == 0:
                conn.execute(
                    "INSERT INTO admins (username, password) VALUES (?, ?)",
                    ("admin", "admin123"),
                )
                conn.commit()

            # Seed sample cars if empty
            if conn.execute("SELECT COUNT(*) FROM cars").fetchone()[0] == 0:
                sample_cars = [
                    ("Toyota", "Camry",      2022, 45.00, "Available", "Silver",  "TN01AB1234"),
                    ("Honda",  "Civic",      2023, 40.00, "Available", "White",   "TN02CD5678"),
                    ("BMW",    "3 Series",   2022, 90.00, "Available", "Black",   "TN03EF9012"),
                    ("Ford",   "Mustang",    2021, 85.00, "Available", "Red",     "TN04GH3456"),
                    ("Tesla",  "Model 3",    2023, 110.00,"Available", "Blue",    "TN05IJ7890"),
                    ("Hyundai","Creta",      2022, 38.00, "Available", "White",   "TN06KL1234"),
                    ("Kia",    "Seltos",     2023, 42.00, "Available", "Grey",    "TN07MN5678"),
                    ("Mahindra","Scorpio N", 2023, 55.00, "Available", "Brown",   "TN08OP9012"),
                ]
                conn.executemany(
                    "INSERT INTO cars (brand,model,year,price_per_day,status,color,plate_number) VALUES (?,?,?,?,?,?,?)",
                    sample_cars,
                )
                conn.commit()

    # ══════════════════════════════════════════════════════════════════════════
    #  ADMIN
    # ══════════════════════════════════════════════════════════════════════════

    def verify_admin(self, username: str, password: str) -> bool:
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT id FROM admins WHERE username=? AND password=?",
                (username, password),
            ).fetchone()
            return row is not None

    def change_password(self, username: str, new_password: str):
        with self.get_connection() as conn:
            conn.execute(
                "UPDATE admins SET password=? WHERE username=?",
                (new_password, username),
            )
            conn.commit()

    # ══════════════════════════════════════════════════════════════════════════
    #  CARS
    # ══════════════════════════════════════════════════════════════════════════

    def add_car(self, brand, model, year, price_per_day, status, color, plate_number):
        with self.get_connection() as conn:
            conn.execute(
                """INSERT INTO cars (brand,model,year,price_per_day,status,color,plate_number)
                   VALUES (?,?,?,?,?,?,?)""",
                (brand, model, year, price_per_day, status, color, plate_number),
            )
            conn.commit()

    def update_car(self, car_id, brand, model, year, price_per_day, status, color, plate_number):
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE cars SET brand=?,model=?,year=?,price_per_day=?,
                   status=?,color=?,plate_number=? WHERE car_id=?""",
                (brand, model, year, price_per_day, status, color, plate_number, car_id),
            )
            conn.commit()

    def delete_car(self, car_id):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM cars WHERE car_id=?", (car_id,))
            conn.commit()

    def get_all_cars(self):
        with self.get_connection() as conn:
            return conn.execute(
                "SELECT car_id,brand,model,year,price_per_day,status,color,plate_number FROM cars ORDER BY car_id"
            ).fetchall()

    def get_car_by_id(self, car_id):
        with self.get_connection() as conn:
            return conn.execute("SELECT * FROM cars WHERE car_id=?", (car_id,)).fetchone()

    def search_cars(self, query: str):
        q = f"%{query}%"
        with self.get_connection() as conn:
            return conn.execute(
                """SELECT car_id,brand,model,year,price_per_day,status,color,plate_number
                   FROM cars
                   WHERE brand LIKE ? OR model LIKE ? OR status LIKE ? OR plate_number LIKE ?
                   ORDER BY car_id""",
                (q, q, q, q),
            ).fetchall()

    def get_available_cars(self):
        with self.get_connection() as conn:
            return conn.execute(
                "SELECT car_id,brand,model,year,price_per_day FROM cars WHERE status='Available' ORDER BY brand"
            ).fetchall()

    def set_car_status(self, car_id, status: str):
        with self.get_connection() as conn:
            conn.execute("UPDATE cars SET status=? WHERE car_id=?", (status, car_id))
            conn.commit()

    # ══════════════════════════════════════════════════════════════════════════
    #  CUSTOMERS
    # ══════════════════════════════════════════════════════════════════════════

    def add_customer(self, name, phone, email, license_number, address):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO customers (name,phone,email,license_number,address) VALUES (?,?,?,?,?)",
                (name, phone, email, license_number, address),
            )
            conn.commit()

    def update_customer(self, customer_id, name, phone, email, license_number, address):
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE customers SET name=?,phone=?,email=?,license_number=?,address=?
                   WHERE customer_id=?""",
                (name, phone, email, license_number, address, customer_id),
            )
            conn.commit()

    def delete_customer(self, customer_id):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM customers WHERE customer_id=?", (customer_id,))
            conn.commit()

    def get_all_customers(self):
        with self.get_connection() as conn:
            return conn.execute(
                "SELECT customer_id,name,phone,email,license_number,address FROM customers ORDER BY name"
            ).fetchall()

    def get_customer_by_id(self, customer_id):
        with self.get_connection() as conn:
            return conn.execute(
                "SELECT * FROM customers WHERE customer_id=?", (customer_id,)
            ).fetchone()

    def search_customers(self, query: str):
        q = f"%{query}%"
        with self.get_connection() as conn:
            return conn.execute(
                """SELECT customer_id,name,phone,email,license_number,address FROM customers
                   WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR license_number LIKE ?
                   ORDER BY name""",
                (q, q, q, q),
            ).fetchall()

    # ══════════════════════════════════════════════════════════════════════════
    #  RENTALS
    # ══════════════════════════════════════════════════════════════════════════

    def add_rental(self, customer_id, car_id, start_date, end_date, total_amount):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO rentals (customer_id,car_id,start_date,end_date,total_amount,status,created_at)
                   VALUES (?,?,?,?,?,'Active',?)""",
                (customer_id, car_id, start_date, end_date, total_amount, now),
            )
            conn.commit()
            return cursor.lastrowid

    def return_car(self, rental_id):
        """Mark rental as Returned, set car back to Available."""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT car_id FROM rentals WHERE rental_id=?", (rental_id,)
            ).fetchone()
            if row:
                conn.execute(
                    "UPDATE rentals SET status='Returned' WHERE rental_id=?", (rental_id,)
                )
                conn.execute(
                    "UPDATE cars SET status='Available' WHERE car_id=?", (row["car_id"],)
                )
                conn.commit()

    def get_all_rentals(self):
        with self.get_connection() as conn:
            return conn.execute(
                """SELECT r.rental_id, c.name AS customer_name, ca.brand||' '||ca.model AS car,
                          r.start_date, r.end_date, r.total_amount, r.status, r.created_at
                   FROM rentals r
                   JOIN customers c  ON c.customer_id = r.customer_id
                   JOIN cars     ca  ON ca.car_id      = r.car_id
                   ORDER BY r.rental_id DESC"""
            ).fetchall()

    def get_rental_by_id(self, rental_id):
        with self.get_connection() as conn:
            return conn.execute(
                """SELECT r.*,
                          c.name AS customer_name, c.phone, c.email, c.license_number,
                          ca.brand, ca.model, ca.year, ca.plate_number, ca.price_per_day
                   FROM rentals r
                   JOIN customers c  ON c.customer_id = r.customer_id
                   JOIN cars     ca  ON ca.car_id      = r.car_id
                   WHERE r.rental_id=?""",
                (rental_id,),
            ).fetchone()

    def search_rentals(self, query: str):
        q = f"%{query}%"
        with self.get_connection() as conn:
            return conn.execute(
                """SELECT r.rental_id, c.name AS customer_name, ca.brand||' '||ca.model AS car,
                          r.start_date, r.end_date, r.total_amount, r.status, r.created_at
                   FROM rentals r
                   JOIN customers c  ON c.customer_id = r.customer_id
                   JOIN cars     ca  ON ca.car_id      = r.car_id
                   WHERE c.name LIKE ? OR ca.brand LIKE ? OR ca.model LIKE ? OR r.status LIKE ?
                   ORDER BY r.rental_id DESC""",
                (q, q, q, q),
            ).fetchall()

    def get_active_rentals(self):
        with self.get_connection() as conn:
            return conn.execute(
                """SELECT r.rental_id, c.name, ca.brand||' '||ca.model, r.start_date, r.end_date, r.total_amount
                   FROM rentals r
                   JOIN customers c  ON c.customer_id = r.customer_id
                   JOIN cars     ca  ON ca.car_id      = r.car_id
                   WHERE r.status='Active'
                   ORDER BY r.rental_id DESC"""
            ).fetchall()

    # ══════════════════════════════════════════════════════════════════════════
    #  DASHBOARD STATS
    # ══════════════════════════════════════════════════════════════════════════

    def get_stats(self) -> dict:
        with self.get_connection() as conn:
            total_cars      = conn.execute("SELECT COUNT(*) FROM cars").fetchone()[0]
            available_cars  = conn.execute("SELECT COUNT(*) FROM cars WHERE status='Available'").fetchone()[0]
            rented_cars     = conn.execute("SELECT COUNT(*) FROM cars WHERE status='Rented'").fetchone()[0]
            total_customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
            active_rentals  = conn.execute("SELECT COUNT(*) FROM rentals WHERE status='Active'").fetchone()[0]
            total_revenue   = conn.execute(
                "SELECT COALESCE(SUM(total_amount),0) FROM rentals WHERE status='Returned'"
            ).fetchone()[0]

            return {
                "total_cars":      total_cars,
                "available_cars":  available_cars,
                "rented_cars":     rented_cars,
                "total_customers": total_customers,
                "active_rentals":  active_rentals,
                "total_revenue":   round(total_revenue, 2),
            }

    def get_recent_rentals(self, limit=10):
        with self.get_connection() as conn:
            return conn.execute(
                """SELECT r.rental_id, c.name, ca.brand||' '||ca.model, r.start_date, r.end_date, r.total_amount, r.status
                   FROM rentals r
                   JOIN customers c  ON c.customer_id = r.customer_id
                   JOIN cars     ca  ON ca.car_id      = r.car_id
                   ORDER BY r.created_at DESC LIMIT ?""",
                (limit,),
            ).fetchall()
