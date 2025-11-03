import tkinter as tk
from tkinter import messagebox
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
        # Ensure all fields are present
        for key in equipment_fields:
            if key not in data:
                data[key] = 0
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {key: 0 for key in equipment_fields}

def on_equipment_manager(root, admin):
    root.title("Equipment Manager")
    text_label = tk.Label(root, text="Equipment Manager", font=("Arial", 24), bg=root["bg"])
    text_label.pack(pady=20)

    main_frame = tk.Frame(root, bg=root["bg"])
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Load equipment data
    equipment_data = load_equipment_data()
    entry_vars = {}

    def make_row(row, name):
        label = tk.Label(main_frame, text=name, bg=root["bg"], font=("Arial", 12))
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        var = tk.IntVar(value=equipment_data.get(name, 0))
        entry = tk.Entry(main_frame, textvariable=var, width=6, font=("Arial", 12), justify="center", state="readonly")
        entry.grid(row=row, column=1, padx=5)
        def increase():
            var.set(var.get() + 1)
        def decrease():
            if var.get() > 0:
                var.set(var.get() - 1)
        inc_btn = tk.Button(main_frame, text="+", command=increase, width=3, font=("Arial", 10, "bold"))
        inc_btn.grid(row=row, column=2, padx=2)
        dec_btn = tk.Button(main_frame, text="-", command=decrease, width=3, font=("Arial", 10, "bold"))
        dec_btn.grid(row=row, column=3, padx=2)
        entry_vars[name] = var

    for i, eq_name in enumerate(equipment_fields):
        make_row(i, eq_name)

    def save():
        new_data = {name: var.get() for name, var in entry_vars.items()}
        # Use admin's method to save equipment data
        if admin.save_equipment_data(new_data):
            messagebox.showinfo("Success", "Equipment data saved successfully!")
        else:
            messagebox.showerror("Error", "Failed to save equipment data!")

    # Button frame for Save and Back buttons
    button_frame = tk.Frame(root, bg=root["bg"])
    button_frame.pack(pady=20)

    save_btn = tk.Button(button_frame, text="Save", command=save, font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", relief="raised", bd=2)
    save_btn.pack(side="left", padx=10)

    def back_to_menu():
        root.destroy()

    back_btn = tk.Button(button_frame, text="Back to Menu", command=back_to_menu,
                        font=("Arial", 14, "bold"), bg="#2196F3", fg="white",
                        relief="raised", bd=2)
    back_btn.pack(side="left", padx=10) 