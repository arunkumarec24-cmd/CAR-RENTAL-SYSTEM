# Car Rental System

A complete modern GUI application built with Python and Tkinter for managing car rentals.

## Features
- **Admin Login System**: Secure authentication for administrators.
- **Dashboard**: Live statistics and recent rental activity.
- **Car Management**: Full CRUD operations with search and filter.
- **Customer Directory**: Manage customer details and driving licenses.
- **Rental System**: Book rentals, auto-calculate costs, and return vehicles.
- **Receipt Generation**: Generate text-based receipts for each rental.
- **Data Export**: Export all tables to CSV.
- **Dark Theme GUI**: Modern, responsive, and professional user interface.
- **SQLite Database**: Auto-initializes schema with default admin and sample data.

## Getting Started

1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```
4. Log in using the default admin credentials:
   - **Username**: admin
   - **Password**: admin123

## Folder Structure
- `main.py`: Application entry point.
- `car_rental.db`: SQLite database file (auto-generated).
- `exports/`: Directory for saved receipts and CSV exports (auto-generated).
- `CAR/`: Main package directory containing GUI and logic modules.
  - `theme.py`: UI styling and colors.
  - `widgets.py`: Reusable UI components.
  - `db_manager.py`: Database operations.
  - `rental_logic.py`: Core business logic.
  - `login_window.py`, `dashboard_tab.py`, `car_tab.py`, `customer_tab.py`, `rental_tab.py`: App screens.
