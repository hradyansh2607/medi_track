# MediTrack: Smart Hospital Supply & Expiry Monitor 🏥💻

MediTrack is an advanced desktop-native healthcare logistics control dashboard built using **100% pure Python**. The project tracks critical medical supplies, monitors volume safety buffers, and handles real-time expiry window alerts to prevent hospital resource waste.

## 🌟 Key Functional Features
- **Native GUI Architecture:** Modern desktop interface window built without mixing HTML or web browser wrappers.
- **Dynamic KPI Panels:** Live-updating indicators counting total active inventory, near-expiry risks, and stock items crossing reorder lines.
- **Interactive Ledger Board:** Sortable multi-column table displaying product details, storage room locations, and specific countdown trackers.
- **Data Modification Engine:** Built-in validation entry panels that allow adding or removing records securely on-the-fly.

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

## 🚀 Execution Instructions
This project has zero third-party package dependencies, as it runs entirely on Python’s native environment standard libraries!

1. Clone your project repository or navigate to your project directory root.
2. Launch the desktop system directly from your terminal console:
   ```bash
   python app.py
   ```
