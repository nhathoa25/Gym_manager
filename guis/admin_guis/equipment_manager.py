import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

equipment_fields = [
    "Dumbells", "Rope", "Balls", "Chest Press", "Incline Chest Press",
    "Big Barbel Rod", "Zik-Zak Rod", "Small Barbel Rod", "Leg Press Machine",
    "Benth", "T.V", "Speeker", "2 kg Weight", "5 kg Weight", "10 kg Weight",
    "20 kg Weight", "30 kg Weight", "50 kg Weight"
]

def load_equipment_data():
    filepath = "data/equipment_info.json"
    if not os.path.exists(filepath):
        return {key: 0 for key in equipment_fields}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key in equipment_fields:
            if key not in data: data[key] = 0
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {key: 0 for key in equipment_fields}

def on_equipment_manager(root, admin):
    text_label = ttk.Label(root, text="Equipment Manager", font=("Arial", 24))
    text_label.pack(pady=20)

    main_frame = ttk.Frame(root)
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Căn giữa lưới
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)
    main_frame.columnconfigure(3, weight=1)
    
    equipment_data = load_equipment_data()
    entry_vars = {}

    def make_row(row, name):
        label = ttk.Label(main_frame, text=name, font=("Arial", 12))
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        
        var = tk.IntVar(value=equipment_data.get(name, 0))
        entry = ttk.Entry(main_frame, textvariable=var, width=6, font=("Arial", 12), justify="center", state="readonly")
        entry.grid(row=row, column=1, padx=5)
        
        def increase(): var.set(var.get() + 1)
        def decrease():
            if var.get() > 0: var.set(var.get() - 1)
            
        inc_btn = tk.Button(main_frame, text="+", command=increase, width=3, font=("Arial", 10, "bold"))
        inc_btn.grid(row=row, column=2, padx=2)
        dec_btn = tk.Button(main_frame, text="-", command=decrease, width=3, font=("Arial", 10, "bold"))
        dec_btn.grid(row=row, column=3, padx=2)
        
        entry_vars[name] = var

    # Chia thành 2 cột
    half_len = (len(equipment_fields) + 1) // 2
    for i in range(half_len):
        make_row(i, equipment_fields[i])
    for i in range(half_len, len(equipment_fields)):
        # Đặt ở cột 5, 6, 7, 8
        eq_name = equipment_fields[i]
        row_index = i - half_len
        
        label = ttk.Label(main_frame, text=eq_name, font=("Arial", 12))
        label.grid(row=row_index, column=5, padx=10, pady=5, sticky="w")
        
        var = tk.IntVar(value=equipment_data.get(eq_name, 0))
        entry = ttk.Entry(main_frame, textvariable=var, width=6, font=("Arial", 12), justify="center", state="readonly")
        entry.grid(row=row_index, column=6, padx=5)
        
        def create_inc_dec(v): # Tránh lỗi closure
            def increase(): v.set(v.get() + 1)
            def decrease():
                if v.get() > 0: v.set(v.get() - 1)
            return increase, decrease
        
        increase, decrease = create_inc_dec(var)
        
        inc_btn = tk.Button(main_frame, text="+", command=increase, width=3, font=("Arial", 10, "bold"))
        inc_btn.grid(row=row_index, column=7, padx=2)
        dec_btn = tk.Button(main_frame, text="-", command=decrease, width=3, font=("Arial", 10, "bold"))
        dec_btn.grid(row=row_index, column=8, padx=2)
        entry_vars[eq_name] = var

    main_frame.columnconfigure(4, weight=1) # Thêm khoảng cách
    main_frame.columnconfigure(9, weight=1) # Thêm khoảng cách


    def save():
        new_data = {name: var.get() for name, var in entry_vars.items()}
        if admin.save_equipment_data(new_data):
            messagebox.showinfo("Success", "Equipment data saved successfully!")
        else:
            messagebox.showerror("Error", "Failed to save equipment data!")

    button_frame = ttk.Frame(root)
    button_frame.pack(side="bottom", pady=20)

    save_btn = ttk.Button(button_frame, text="Save", command=save, style="Success.TButton")
    save_btn.pack(side="left", padx=10)

    back_btn = ttk.Button(button_frame, text="Back to Menu", command=root.destroy, style="Primary.TButton")
    back_btn.pack(side="left", padx=10)