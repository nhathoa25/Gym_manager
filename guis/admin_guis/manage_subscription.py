import tkinter as tk
from tkinter import messagebox
import json
import os

def load_subscription_data():
    filepath = "data/subscription_info.json"
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def on_manage_subscription(root, admin):
    root.title("Manage Subscription Plans")
    text_label = tk.Label(root, text="Manage Subscription Plans", font=("Arial", 24), bg=root["bg"])
    text_label.pack(pady=20)

    main_frame = tk.Frame(root, bg=root["bg"])
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Load subscription data
    subscription_data = load_subscription_data()
    entry_vars = {}
    plan_frames = {}  # Store frame references for dynamic updates

    # Create a frame for the subscription plans
    plans_frame = tk.Frame(main_frame, bg=root["bg"])
    plans_frame.pack(pady=10)

    # Header
    header_label = tk.Label(plans_frame, text="Subscription Plans, Durations (days) and Fees", 
                           font=("Arial", 16, "bold"), bg=root["bg"])
    header_label.pack(pady=10)

    # Create a scrollable frame for plans
    canvas = tk.Canvas(plans_frame, bg=root["bg"], height=300)
    scrollbar = tk.Scrollbar(plans_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=root["bg"])

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def create_plan_row(plan_name, duration, fee, is_new=False):
        """Create a row for a subscription plan"""
        plan_frame = tk.Frame(scrollable_frame, bg=root["bg"])
        plan_frame.pack(pady=5, fill="x")
        
        plan_label = tk.Label(plan_frame, text=f"{plan_name}:", 
                             font=("Arial", 12), bg=root["bg"], width=15, anchor="w")
        plan_label.pack(side="left", padx=10)
        
        # Duration entry
        duration_var = tk.IntVar(value=duration)
        duration_entry = tk.Entry(plan_frame, textvariable=duration_var, width=8, 
                        font=("Arial", 12), justify="center")
        duration_entry.pack(side="left", padx=5)
        
        days_label = tk.Label(plan_frame, text="days", 
                             font=("Arial", 12), bg=root["bg"])
        days_label.pack(side="left", padx=5)
        
        # Fee entry
        fee_var = tk.IntVar(value=fee)
        fee_entry = tk.Entry(plan_frame, textvariable=fee_var, width=12, 
                        font=("Arial", 12), justify="center")
        fee_entry.pack(side="left", padx=5)
        
        fee_label = tk.Label(plan_frame, text="VND", 
                             font=("Arial", 12), bg=root["bg"])
        fee_label.pack(side="left", padx=5)
        
        # Add delete button for new plans
        if is_new:
            def delete_plan():
                plan_frame.destroy()
                if plan_name in entry_vars:
                    del entry_vars[plan_name]
                if plan_name in plan_frames:
                    del plan_frames[plan_name]
            
            delete_btn = tk.Button(plan_frame, text="✕", command=delete_plan,
                                 font=("Arial", 10, "bold"), bg="#ff4444", fg="white",
                                 width=3, height=1)
            delete_btn.pack(side="right", padx=5)
        
        entry_vars[plan_name] = {"duration": duration_var, "fee": fee_var}
        plan_frames[plan_name] = plan_frame
        return plan_frame

    # Create entries for existing subscription plans
    for plan_name, plan_data in subscription_data.items():
        if isinstance(plan_data, list) and len(plan_data) >= 2:
            duration = plan_data[0]
            fee = plan_data[1]
            create_plan_row(plan_name, duration, fee, is_new=False)
        else:
            # Handle legacy data format or invalid data
            duration = 30
            fee = 1000000
            create_plan_row(plan_name, duration, fee, is_new=False)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add new plan section
    add_frame = tk.Frame(main_frame, bg=root["bg"])
    add_frame.pack(pady=20)

    add_label = tk.Label(add_frame, text="Add New Subscription Plan", 
                        font=("Arial", 16, "bold"), bg=root["bg"])
    add_label.pack(pady=10)

    new_plan_frame = tk.Frame(add_frame, bg=root["bg"])
    new_plan_frame.pack(pady=5)

    tk.Label(new_plan_frame, text="Plan Name:", font=("Arial", 12), bg=root["bg"]).pack(side="left", padx=5)
    new_plan_name = tk.Entry(new_plan_frame, font=("Arial", 12), width=15)
    new_plan_name.pack(side="left", padx=5)

    tk.Label(new_plan_frame, text="Duration (days):", font=("Arial", 12), bg=root["bg"]).pack(side="left", padx=5)
    new_plan_duration = tk.Entry(new_plan_frame, font=("Arial", 12), width=10)
    new_plan_duration.pack(side="left", padx=5)

    tk.Label(new_plan_frame, text="Fee (VND):", font=("Arial", 12), bg=root["bg"]).pack(side="left", padx=5)
    new_plan_fee = tk.Entry(new_plan_frame, font=("Arial", 12), width=12)
    new_plan_fee.pack(side="left", padx=5)

    def add_new_plan():
        plan_name = new_plan_name.get().strip()
        duration_str = new_plan_duration.get().strip()
        fee_str = new_plan_fee.get().strip()
        
        if not plan_name:
            messagebox.showerror("Error", "Please enter a plan name!")
            return
        
        if not duration_str:
            messagebox.showerror("Error", "Please enter a duration!")
            return
        
        if not fee_str:
            messagebox.showerror("Error", "Please enter a fee!")
            return
        
        try:
            duration = int(duration_str)
            if duration <= 0:
                messagebox.showerror("Error", "Duration must be a positive number!")
                return
        except ValueError:
            messagebox.showerror("Error", "Duration must be a valid number!")
            return
        
        try:
            fee = int(fee_str)
            if fee < 0:
                messagebox.showerror("Error", "Fee must be a non-negative number!")
                return
        except ValueError:
            messagebox.showerror("Error", "Fee must be a valid number!")
            return
        
        if plan_name in entry_vars:
            messagebox.showerror("Error", "Plan name already exists!")
            return
        
        # Create new row in GUI
        create_plan_row(plan_name, duration, fee, is_new=True)
        
        # Clear input fields
        new_plan_name.delete(0, tk.END)
        new_plan_duration.delete(0, tk.END)
        new_plan_fee.delete(0, tk.END)
        
        

    add_btn = tk.Button(add_frame, text="Add Plan", command=add_new_plan,
                       font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
    add_btn.pack(pady=10)

    def save():
        new_data = {}
        for name, vars_dict in entry_vars.items():
            duration = vars_dict["duration"].get()
            fee = vars_dict["fee"].get()
            new_data[name] = [duration, fee]
        
        print(f"Saving data: {new_data}")  # Debug print
        
        # Use admin's method to save subscription data
        if admin.save_subscription_data(new_data):
            messagebox.showinfo("Success", "Subscription data saved successfully!")
            # Refresh the data
            global subscription_data
            subscription_data = new_data
        else:
            messagebox.showerror("Error", "Failed to save subscription data!")

    # Button frame for Save and Back buttons
    button_frame = tk.Frame(root, bg=root["bg"])
    button_frame.pack(pady=20)

    save_btn = tk.Button(button_frame, text="Save Changes", command=save, 
                        font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", 
                        relief="raised", bd=2)
    save_btn.pack(side="left", padx=10)

    def back_to_menu():
        root.destroy()

    back_btn = tk.Button(button_frame, text="Back to Menu", command=back_to_menu,
                        font=("Arial", 14, "bold"), bg="#2196F3", fg="white",
                        relief="raised", bd=2)
    back_btn.pack(side="left", padx=10)
