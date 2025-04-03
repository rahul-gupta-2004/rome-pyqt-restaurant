Overview
This is a PyQt-based desktop application for restaurants to manage orders, tables, inventory, and sales reports.

Features
* Room & Table Management: CRUD operations with QR code generation.
* Inventory Management: Add/update/delete food items and manage stock levels.
* Order Management: Take and track orders per table.
* Sales Reporting: Generate reports (daily, weekly, monthly, department-wise, item-wise).
* User Management: Roles - Admin, Owner, Employee/Waiter.

Installation & Setup
1. Install dependencies:
```
pip install -r requirements.txt
```
Run the application:
```
python main.py
```

File Structure
```main.py``` - Entry point for the application.
```tables.py``` - Handles table and QR code management.
```inventory.py``` - Manages stock and product CRUD operations.
```orders.py``` - Handles order-taking and processing.
```reports.py``` - Generates sales reports.
```database/``` - Contains MySQL database connection files.
```assets/``` - Icons, images, and other UI assets.
