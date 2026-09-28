from datetime import datetime, timedelta

today = datetime.now()
exp_critical = (today + timedelta(days=12)).strftime("%Y-%m-%d")
exp_warning = (today + timedelta(days=45)).strftime("%Y-%m-%d")
exp_safe = (today + timedelta(days=240)).strftime("%Y-%m-%d")

medical_inventory = [
    { "id": "1", "name": "Amoxicillin 500mg", "batch": "AMX-2026-09", "category": "Antibiotic", "stock": 120, "min_required": 50, "expiry_date": exp_critical, "room": "Pharmacy-A" },
    { "id": "2", "name": "Epinephrine Auto-Injector", "batch": "EPI-994", "category": "Emergency", "stock": 14, "min_required": 20, "expiry_date": exp_safe, "room": "ER-Tray 1" },
    { "id": "3", "name": "Surgical Gloves (Size 7.5)", "batch": "GLV-002", "category": "Consumables", "stock": 450, "min_required": 100, "expiry_date": "2029-12-31", "room": "Main Store" },
    { "id": "4", "name": "Insulin Glargine 100 U/mL", "batch": "INS-772", "category": "Diabetes Care", "stock": 35, "min_required": 15, "expiry_date": exp_warning, "room": "Cold Storage" },
    { "id": "5", "name": "Paracetamol 500mg IV", "batch": "PCM-441", "category": "Analgesic", "stock": 8, "min_required": 30, "expiry_date": exp_safe, "room": "ICU-Cabinet" }
]

def calculate_metrics():
    """Computes tracking summary parameters dynamically from database arrays."""
    total = len(medical_inventory)
    crit_exp = 0
    low_stock = 0
    
    for item in medical_inventory:
        try:
            exp_date = datetime.strptime(item["expiry_date"], "%Y-%m-%d")
            days_left = (exp_date - datetime.now()).days
            if days_left <= 30:
                crit_exp += 1
        except ValueError:
            pass # Handle fallback formatting
            
        if item["stock"] <= item["min_required"]:
            low_stock += 1
            
    return total, crit_exp, low_stock

def add_new_item(name, batch, category, stock, min_req, expiry, room):
    """Injects a new product dictionary map item cleanly into inventory array."""
    new_id = str(len(medical_inventory) + 1)
    new_record = {
        "id": new_id, "name": name, "batch": batch, "category": category,
        "stock": int(stock), "min_required": int(min_req), "expiry_date": expiry, "room": room
    }
    medical_inventory.append(new_record)
    return True

def remove_item_by_name_and_batch(name, batch):
    """Filters matching identity attributes to wipe records out safely."""
    global medical_inventory
    medical_inventory = [p for p in medical_inventory if not (p["name"] == name and p["batch"] == batch)]
