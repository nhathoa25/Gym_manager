import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

def load_subscription_data():
    filepath = "data/subscription_info.json"
    if not os.path.exists(filepath): return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def on_manage_subscription(root, admin):
    text_label = ttk.Label(root, text="Manage Subscription Plans", font=("Arial", 24))
    text_label.pack(pady=20)

    main_frame = ttk.Frame(root)
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    subscription_data = load_subscription_data()
    entry_vars = {}
    plan_frames = {}

    plans_frame = ttk.Frame(main_frame)
    plans_frame.pack(pady=10)

    header_label = ttk.Label(plans_frame, text="Subscription Plans, Durations (days) and Fees", 
                           font=("Arial", 16, "bold"))
    header_label.pack(pady=10)

    # Khung cuộn
    scroll_container = ttk.Frame(plans_frame)
    scroll_container.pack(fill="both", expand=True)
    
    canvas = tk.Canvas(scroll_container, bg=root["bg"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"), width=e.width)
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=20)
    scrollbar.pack(side="right", fill="y")

    def create_plan_row(plan_name, duration, fee, is_new=False):
        plan_frame = ttk.Frame(scrollable_frame)
        plan_frame.pack(pady=5, fill="x")
        
        plan_label = ttk.Label(plan_frame, text=f"{plan_name}:", 
                             font=("Arial", 12), width=15, anchor="w")
        plan_label.pack(side="left", padx=10)
        
        duration_var = tk.IntVar(value=duration)
        duration_entry = ttk.Entry(plan_frame, textvariable=duration_var, width=8, 
                        font=("Arial", 12), justify="center")
        duration_entry.pack(side="left", padx=5)
        
        days_label = ttk.Label(plan_frame, text="days", font=("Arial", 12))
        days_label.pack(side="left", padx=5)
        
        fee_var = tk.IntVar(value=fee)
        fee_entry = ttk.Entry(plan_frame, textvariable=fee_var, width=12, 
                        font=("Arial", 12), justify="center")
        fee_entry.pack(side="left", padx=5)
        
        fee_label = ttk.Label(plan_frame, text="VND", font=("Arial", 12))
        fee_label.pack(side="left", padx=5)
        
        if is_new:
            def delete_plan():
                plan_frame.destroy()
                if plan_name in entry_vars: del entry_vars[plan_name]
                if plan_name in plan_frames: del plan_frames[plan_name]
            
            # Sử dụng style "Danger" nhỏ
            style = ttk.Style()
            style.configure("Small.Danger.TButton", font=("Arial", 10, "bold"), padding=(2, 0))
            style.map("Small.Danger.TButton", 
                      background=[('active', '#d32f2f'), ('!active', '#f44336')],
                      foreground=[('!disabled', 'white')])

            delete_btn = ttk.Button(plan_frame, text="✕", command=delete_plan,
                                  style="Small.Danger.TButton", width=3)
            delete_btn.pack(side="right", padx=5)
        
        entry_vars[plan_name] = {"duration": duration_var, "fee": fee_var}
        plan_frames[plan_name] = plan_frame
        return plan_frame

    for plan_name, plan_data in subscription_data.items():
        if isinstance(plan_data, list) and len(plan_data) >= 2:
            duration, fee = plan_data[0], plan_data[1]
        else: # Xử lý dữ liệu cũ/lỗi
            duration, fee = 30, 1000000
        create_plan_row(plan_name, duration, fee, is_new=False)


    # Thêm plan mới
    add_frame = ttk.Frame(main_frame)
    add_frame.pack(pady=20)

    add_label = ttk.Label(add_frame, text="Add New Subscription Plan", 
                        font=("Arial", 16, "bold"))
    add_label.pack(pady=10)

    new_plan_frame = ttk.Frame(add_frame)
    new_plan_frame.pack(pady=5)

    ttk.Label(new_plan_frame, text="Plan Name:", font=("Arial", 12)).pack(side="left", padx=5)
    new_plan_name = ttk.Entry(new_plan_frame, font=("Arial", 12), width=15)
    new_plan_name.pack(side="left", padx=5)

    ttk.Label(new_plan_frame, text="Duration (days):", font=("Arial", 12)).pack(side="left", padx=5)
    new_plan_duration = ttk.Entry(new_plan_frame, font=("Arial", 12), width=10)
    new_plan_duration.pack(side="left", padx=5)

    ttk.Label(new_plan_frame, text="Fee (VND):", font=("Arial", 12)).pack(side="left", padx=5)
    new_plan_fee = ttk.Entry(new_plan_frame, font=("Arial", 12), width=12)
    new_plan_fee.pack(side="left", padx=5)

    def add_new_plan():
        plan_name = new_plan_name.get().strip()
        duration_str = new_plan_duration.get().strip()
        fee_str = new_plan_fee.get().strip()
        
        if not all([plan_name, duration_str, fee_str]):
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        try: duration = int(duration_str)
        except ValueError:
            messagebox.showerror("Error", "Duration must be a valid number!")
            return
        
        try: fee = int(fee_str)
        except ValueError:
            messagebox.showerror("Error", "Fee must be a valid number!")
            return

        if duration <= 0 or fee < 0:
            messagebox.showerror("Error", "Duration and Fee must be positive numbers!")
            return
        
        if plan_name in entry_vars:
            messagebox.showerror("Error", "Plan name already exists!")
            return
        
        create_plan_row(plan_name, duration, fee, is_new=True)
        new_plan_name.delete(0, tk.END)
        new_plan_duration.delete(0, tk.END)
        new_plan_fee.delete(0, tk.END)

    add_btn = ttk.Button(add_frame, text="Add Plan", command=add_new_plan, style="Success.TButton")
    add_btn.pack(pady=10)

    def save():
        new_data = {}
        for name, vars_dict in entry_vars.items():
            try:
                duration = vars_dict["duration"].get()
                fee = vars_dict["fee"].get()
                new_data[name] = [duration, fee]
            except Exception:
                messagebox.showerror("Error", f"Invalid data for plan '{name}'. Please check.")
                return
        
        if admin.save_subscription_data(new_data):
            messagebox.showinfo("Success", "Subscription data saved successfully!")
            global subscription_data
            subscription_data = new_data
        else:
            messagebox.showerror("Error", "Failed to save subscription data!")

    button_frame = ttk.Frame(root)
    button_frame.pack(side="bottom", pady=20)

    save_btn = ttk.Button(button_frame, text="Save Changes", command=save, style="Success.TButton")
    save_btn.pack(side="left", padx=10)

    back_btn = ttk.Button(button_frame, text="Back to Menu", command=root.destroy, style="Primary.TButton")
    back_btn.pack(side="left", padx=10)