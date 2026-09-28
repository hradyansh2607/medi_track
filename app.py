import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from core.database import medical_inventory, calculate_metrics, add_new_item, remove_item_by_name_and_batch

class MediTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MediTrack // Hospital Supply & Expiry Monitor")
        self.root.geometry("1100x600")
        self.root.configure(bg="#1e293b")

        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#334155", foreground="#f8fafc", fieldbackground="#334155", rowheight=28)
        style.map("Treeview", background=[('selected', '#6366f1')])
        style.configure("Treeview.Heading", background="#475569", foreground="#ffffff", font=('Arial', 10, 'bold'))

        header_frame = tk.Frame(self.root, bg="#0f172a", height=60)
        header_frame.pack(fill="x", side="top")
        
        title_label = tk.Label(header_frame, text="🏥 MediTrack Management System", font=("Arial", 14, "bold"), fg="#f43f5e", bg="#0f172a")
        title_label.pack(side="left", padx=20, pady=15)
        
        self.status_lbl = tk.Label(header_frame, text="System Status: Connected", font=("Courier", 10), fg="#34d399", bg="#0f172a")
        self.status_lbl.pack(side="right", padx=20, pady=15)

    
        self.kpi_frame = tk.Frame(self.root, bg="#1e293b")
        self.kpi_frame.pack(fill="x", padx=20, pady=10)
        self.render_kpi_panels()

        
        main_body = tk.Frame(self.root, bg="#1e293b")
        main_body.pack(fill="both", expand=True, padx=20, pady=10)

        
        left_frame = tk.Frame(main_body, bg="#1e293b")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        columns = ("name", "batch", "category", "stock", "expiry", "risk")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings")
        
        self.tree.heading("name", text="Medical Item Name")
        self.tree.heading("batch", text="Batch ID")
        self.tree.heading("category", text="Category")
        self.tree.heading("stock", text="Stock / Min")
        self.tree.heading("expiry", text="Expiry Date")
        self.tree.heading("risk", text="Risk Status")

        self.tree.column("name", width=180, anchor="w")
        self.tree.column("batch", width=80, anchor="center")
        self.tree.column("category", width=100, anchor="center")
        self.tree.column("stock", width=90, anchor="center")
        self.tree.column("expiry", width=110, anchor="center")
        self.tree.column("risk", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

       
        btn_delete = tk.Button(left_frame, text="🗑 Remove Selected Supply Record", font=("Arial", 10, "bold"), bg="#ef4444", fg="white", activebackground="#dc2626", activeforeground="white", command=self.handle_delete_action)
        btn_delete.pack(fill="x", pady=10)

        
        right_frame = tk.Frame(main_body, bg="#334155", bd=1, relief="solid", highlightbackground="#475569")
        right_frame.pack(side="right", fill="both", padx=(10, 0), ipady=20)
        
        form_title = tk.Label(right_frame, text="➕ Add New Supply Record", font=("Arial", 11, "bold"), fg="#ffffff", bg="#334155")
        form_title.pack(anchor="w", padx=15, pady=15)

        
        self.ent_name = self.create_form_field(right_frame, "Item Product Name:")
        self.ent_batch = self.create_form_field(right_frame, "Batch Identifier Code:")
        self.ent_cat = self.create_form_field(right_frame, "Category Class:")
        self.ent_stock = self.create_form_field(right_frame, "Current Pack Vol Quantity:")
        self.ent_min = self.create_form_field(right_frame, "Safety Buffer Threshold Limit:")
        self.ent_exp = self.create_form_field(right_frame, "Expiry Date Target (YYYY-MM-DD):")
        self.ent_room = self.create_form_field(right_frame, "Target Inventory Storage Location:")

        # Inject default boilerplate layout format text helper indicators
        self.ent_exp.insert(0, datetime.now().strftime("%Y-%m-%d"))

        btn_submit = tk.Button(right_frame, text="💾 Commit Entry To Ledger", font=("Arial", 10, "bold"), bg="#10b981", fg="white", activebackground="#059669", activeforeground="white", command=self.handle_form_submission)
        btn_submit.pack(fill="x", padx=15, pady=20)

        self.load_inventory_records()

    def create_form_field(self, parent, label_text):
        """Helper matrix generating clean input parameters blocks consistently."""
        lbl = tk.Label(parent, text=label_text, font=("Arial", 9), fg="#cbd5e1", bg="#334155")
        lbl.pack(anchor="w", padx=15, pady=(5, 2))
        entry = tk.Entry(parent, font=("Arial", 10), bg="#1e293b", fg="white", insertbackground="white", bd=1, relief="solid")
        entry.pack(fill="x", padx=15, ipady=3)
        return entry

    def render_kpi_panels(self):
        """Re-draws card tracking data objects dynamically."""
        for widget in self.kpi_frame.winfo_children():
            widget.destroy()
            
        total, critical, low = calculate_metrics()
        self.create_kpi_card(self.kpi_frame, "TOTAL ITEMS", str(total), "#3b82f6", 0)
        self.create_kpi_card(self.kpi_frame, "CRITICAL EXPIRIES", str(critical), "#ef4444", 1)
        self.create_kpi_card(self.kpi_frame, "LOW STOCK ALERTS", str(low), "#f59e0b", 2)

    def create_kpi_card(self, parent, title, value, color, idx):
        card = tk.Frame(parent, bg="#334155", highlightbackground="#475569", highlightthickness=1)
        card.grid(row=0, column=idx, padx=10, sticky="nsew")
        parent.grid_columnconfigure(idx, weight=1)
        
        tk.Label(card, text=title, font=("Arial", 9, "bold"), fg="#94a3b8", bg="#334155").pack(anchor="w", padx=15, pady=(8, 2))
        tk.Label(card, text=value, font=("Arial", 18, "bold"), fg=color, bg="#334155").pack(anchor="w", padx=15, pady=(0, 8))

    def load_inventory_records(self):
        """Wipes table clear and pulls accurate listings from core database mapping."""
        for record in self.tree.get_children():
            self.tree.delete(record)
            
        for item in medical_inventory:
            try:
                exp_date = datetime.strptime(item["expiry_date"], "%Y-%m-%d")
                days_left = (exp_date - datetime.now()).days
                risk = "🟢 SECURE"
                if days_left <= 30: risk = "🔴 HIGH RISK"
                elif days_left <= 90: risk = "🟡 MED RISK"
                exp_str = f"{item['expiry_date']} ({days_left}d)"
            except ValueError:
                risk = "⚠️ INVALID DATE"
                exp_str = item["expiry_date"]

            stock_display = f"{item['stock']} / {item['min_required']}"
            if item['stock'] <= item['min_required']: stock_display += " ⚠️"

            self.tree.insert("", "end", values=(item["name"], item["batch"], item["category"], stock_display, exp_str, risk))

    def handle_form_submission(self):
        """Validates variables input matrices and commits data arrays."""
        name = self.ent_name.get().strip()
        batch = self.ent_batch.get().strip()
        cat = self.ent_cat.get().strip()
        stock = self.ent_stock.get().strip()
        min_req = self.ent_min.get().strip()
        exp = self.ent_exp.get().strip()
        room = self.ent_room.get().strip()

        if not (name and batch and cat and stock and min_req and exp and room):
            messagebox.showwarning("Validation Error", "All supply field attributes must contain data points.")
            return

        try:
            int(stock)
            int(min_req)
            datetime.strptime(exp, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Format Parsing Exception", "Stock/Min must be integers. Expiry date format rule: YYYY-MM-DD.")
            return

        add_new_item(name, batch, cat, stock, min_req, exp, room)
        
    
        self.ent_name.delete(0, tk.END)
        self.ent_batch.delete(0, tk.END)
        self.ent_cat.delete(0, tk.END)
        self.ent_stock.delete(0, tk.END)
        self.ent_min.delete(0, tk.END)
        self.ent_room.delete(0, tk.END)

        # Refresh interface views
        self.render_kpi_panels()
        self.load_inventory_records()
        messagebox.showinfo("Success", f"Product '{name}' saved into ledger configuration database successfully.")

    def handle_delete_action(self):
        """Identifies target highlighted node values and removes row bindings."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Context Missing", "Please select a valid record row element from the tree grid list to remove.")
            return

        row_values = self.tree.item(selected_item[0], 'values')
        name_target = row_values[0]
        batch_target = row_values[1]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently erase the supply log item for: {name_target}?")
        if confirm:
            remove_item_by_name_and_batch(name_target, batch_target)
            self.render_kpi_panels()
            self.load_inventory_records()
            messagebox.showinfo("Ledger Altered", f"Successfully deleted target reference mapping log row.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MediTrackApp(root)
    root.mainloop()
