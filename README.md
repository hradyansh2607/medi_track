Medi Track: Smart Hospital Supply & Expiry Monitor

About the project (overview) Meditrack is a desktop-native healthcare logistics control dashboard entirely developed in Python, used for tracking essential medical commodities, volume safety buffers, and managing real-time expiry window alerts to ensure no hospital resources go to waste.

Key Functional Features

Indigenous GUI Architecture: Interface window for desk-top that is contemporary and that is designed solely for the desktop, developed without HTML or web browser wrappers.
Real-time KPI Panels Live real-time counters showing the number of total live inventory, near expiry risk, and Stock level item or line crosses reorder point.
Interactive Ledger Board: Sortable multi-column table that shows product by product detail, storage room locations, and individual countdown trackers.
Data Modification Engine: Validation entry panels that you can use to add or delete a record.


## 🛠️ Project File Architecture
```text
meditrack/
│
├── core/
│   ├── __init__.py    # Initializer making core a Python package
│   └── database.py    # Holds inventory records array and status calculations
│
├── app.py             # Main GUI application entry point (Tkinter frame controller)
└── README.md          # Technical documentation and launch setup guide
```


Execution Instructions

This project has zero third-party package dependencies, since it relies 100% on the standard libraries in the Python's built-in environment!

Clone the project repository for your organization or go to the root directory of your project.
•Boot desktop straight from your terminal console•
   ```
