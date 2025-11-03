import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from models.admin import Admin
import json


def load_trainers():
    try:
        with open("data/trainer_info.json", "r", encoding="utf-8") as f:
            trainers = json.load(f)
        # List of tuples: (username, display_name)
        return [(t["username"], t.get("name") or f"{t.get('f_name', '')} {t.get('l_name', '')}".strip()) for t in trainers]
    except Exception:
        return []

def on_new_member(root, admin):
    text_label = tk.Label(root, text="New member", font=("Arial", 24), bg=root["bg"])
    text_label.place(relx=0.5, rely=0.1, anchor="n")

    # Create main frame for better organization
    main_frame = tk.Frame(root, bg=root["bg"])
    main_frame.place(relx=0.5, rely=0.2, anchor="n", relwidth=0.8, relheight=0.7)

    # Define fields and their labels
    fields = [
        ("First Name", "f_name", "entry"),
        ("Last Name", "l_name", "entry"),
        ("Phone", "phone", "entry"),
        ("Address", "address", "entry"),
        ("Email", "email", "entry"),
        ("Username", "username", "entry"),
    ]

    entries = {}
    start_y = 0.05
    step_y = 0.08

    # Create regular entry fields
    for i, (label_text, key, field_type) in enumerate(fields):
        y = start_y + i * step_y
        label = tk.Label(main_frame, text=label_text, bg=root["bg"], font=("Arial", 10))
        label.place(relx=0.1, rely=y, anchor="w")
        
        if field_type == "entry":
            entry = tk.Entry(main_frame, font=("Arial", 10))
            entry.place(relx=0.4, rely=y, anchor="w", width=200)
            entries[key] = entry

    # Gender selection with radio buttons
    gender_label = tk.Label(main_frame, text="Gender", bg=root["bg"], font=("Arial", 10))
    gender_label.place(relx=0.1, rely=start_y + len(fields) * step_y, anchor="w")
    
    gender_var = tk.StringVar(value="male")
    gender_frame = tk.Frame(main_frame, bg=root["bg"])
    gender_frame.place(relx=0.4, rely=start_y + len(fields) * step_y, anchor="w")
    
    male_radio = tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="male", bg=root["bg"])
    male_radio.pack(side="left", padx=(0, 20))
    female_radio = tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="female", bg=root["bg"])
    female_radio.pack(side="left")
    entries["gender"] = gender_var

    # Date of Birth calendar
    dob_label = tk.Label(main_frame, text="Date of Birth", bg=root["bg"], font=("Arial", 10))
    dob_label.place(relx=0.1, rely=start_y + (len(fields) + 1) * step_y, anchor="w")
    
    dob_calendar = DateEntry(main_frame, width=20, background='darkblue', foreground='white', 
                           borderwidth=2, date_pattern='yyyy-mm-dd', maxdate=datetime.now(),
                           year=2000, month=1, day=1, firstweekday='sunday',
                           showweeknumbers=False, selectmode='day')
    dob_calendar.place(relx=0.4, rely=start_y + (len(fields) + 1) * step_y, anchor="w")
    entries["date_of_birth"] = dob_calendar

    # Joined Date calendar
    joined_label = tk.Label(main_frame, text="Joined Date", bg=root["bg"], font=("Arial", 10))
    joined_label.place(relx=0.1, rely=start_y + (len(fields) + 2) * step_y, anchor="w")
    
    joined_calendar = DateEntry(main_frame, width=20, background='darkblue', foreground='white', 
                              borderwidth=2, date_pattern='yyyy-mm-dd', maxdate=datetime.now(),
                              year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                              firstweekday='sunday', showweeknumbers=False, selectmode='day')
    joined_calendar.place(relx=0.4, rely=start_y + (len(fields) + 2) * step_y, anchor="w")
    entries["joined_date"] = joined_calendar

    # Membership dropdown - dynamically populated from subscription data
    membership_label = tk.Label(main_frame, text="Membership", bg=root["bg"], font=("Arial", 10))
    membership_label.place(relx=0.1, rely=start_y + (len(fields) + 3) * step_y, anchor="w")
    
    # Get membership options from subscription data
    subscription_data = read_subscription_info()
    membership_options = list(subscription_data.keys()) if subscription_data else ["1 Months"]
    
    membership_var = tk.StringVar(value=membership_options[0] if membership_options else "")
    membership_dropdown = ttk.Combobox(main_frame, textvariable=membership_var, values=membership_options, 
                                      state="readonly", width=17)
    membership_dropdown.place(relx=0.4, rely=start_y + (len(fields) + 3) * step_y, anchor="w")
    entries["membership"] = membership_var

    # Trainer selection
    trainer_label = tk.Label(main_frame, text="Trainer Username", bg=root["bg"], font=("Arial", 10))
    trainer_label.place(relx=0.1, rely=start_y + (len(fields) + 4) * step_y, anchor="w")
    trainer_list = load_trainers()
    trainer_usernames = [t[0] for t in trainer_list]
    trainer_display = [f"{t[1]} ({t[0]})" for t in trainer_list]
    trainer_var = tk.StringVar(value=trainer_usernames[0] if trainer_usernames else "")
    trainer_dropdown = ttk.Combobox(main_frame, textvariable=trainer_var, values=trainer_usernames, state="readonly", width=17)
    trainer_dropdown.place(relx=0.4, rely=start_y + (len(fields) + 4) * step_y, anchor="w")
    entries["trainer_username"] = trainer_var

    # Subscription expiry (auto-calculated based on membership)
    expiry_label = tk.Label(main_frame, text="Subscription Expiry", bg=root["bg"], font=("Arial", 10))
    expiry_label.place(relx=0.1, rely=start_y + (len(fields) + 5) * step_y, anchor="w")
    
    expiry_calendar = DateEntry(main_frame, width=20, background='darkblue', foreground='white', 
                               borderwidth=2, date_pattern='yyyy-mm-dd',
                               year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                               firstweekday='sunday', showweeknumbers=False, selectmode='day')
    expiry_calendar.place(relx=0.4, rely=start_y + (len(fields) + 5) * step_y, anchor="w")
    entries["subscription_expiry"] = expiry_calendar

    def update_expiry_date(*args):
        """Update subscription expiry date based on membership selection"""
        membership = membership_var.get()
        joined_date = joined_calendar.get_date()
        
        # Parse membership duration from subscription data
        duration_map = read_subscription_info()
        print(duration_map)
        if membership in duration_map:
            days = duration_map[membership]
            
        
        expiry_date = joined_date + timedelta(days=days)
        expiry_calendar.set_date(expiry_date)

    # Bind membership dropdown to update expiry date
    membership_var.trace('w', update_expiry_date)
    # Bind joined date calendar to update expiry date
    joined_calendar.bind("<<DateEntrySelected>>", lambda e: update_expiry_date())

    # Set initial values and update expiry date
    joined_calendar.set_date(datetime.now())
    membership_var.set(membership_options[0] if membership_options else "")
    update_expiry_date()

    def submit():
        update_expiry_date()
        values = {}
        for key, entry in entries.items():
            if key == "gender":
                values[key] = entry.get()
            elif key in ["date_of_birth", "joined_date", "subscription_expiry"]:
                values[key] = entry.get_date().strftime('%Y-%m-%d')
            else:
                values[key] = entry.get()
        # Add missing fields
        values["name"] = f"{values.get('f_name', '')} {values.get('l_name', '')}".strip()
        values["attendance_days"] = []
        values["workout_days"] = []
        if any(v == "" for k, v in values.items() if k not in ["attendance_days", "workout_days"]):
            messagebox.showerror("Error", "All fields must be filled!")
            return
        if admin.new_member(values):
            messagebox.showinfo("Success", "Member added successfully!")
            # Clear all fields after successful submission
            for key, entry in entries.items():
                if key == "gender":
                    entry.set("male")
                elif key in ["date_of_birth", "joined_date", "subscription_expiry"]:
                    entry.set_date(datetime.now())
                elif key == "membership":
                    entry.set(membership_options[0] if membership_options else "")
                elif key == "trainer_username":
                    entry.set(trainer_usernames[0] if trainer_usernames else "")
                else:
                    entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to add member. Please try again.")

    # Button frame for Submit and Back buttons
    button_frame = tk.Frame(root, bg=root["bg"])
    # Đặt button_frame ở dưới cùng của form, dùng relx=0.5 và rely=0.98 để luôn nằm cuối form
    button_frame.place(relx=0.5, rely=0.98, anchor="s")

    submit_btn = tk.Button(button_frame, text="Submit", command=submit, 
                          font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
                          relief="raised", bd=2)
    submit_btn.pack(side="left", padx=10)

    def back_to_menu():
        root.destroy()

    back_btn = tk.Button(button_frame, text="Back to Menu", command=back_to_menu,
                        font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
                        relief="raised", bd=2)
    back_btn.pack(side="left", padx=10)

def read_subscription_info():
    """Read subscription information and return duration mapping"""
    try:
        with open("data/subscription_info.json", 'r') as f:
            subscription_data = json.load(f)
        
        # Convert to duration mapping for backward compatibility
        duration_map = {}
        for plan_name, plan_data in subscription_data.items():
            if isinstance(plan_data, list) and len(plan_data) >= 1:
                duration_map[plan_name] = plan_data[0]  # First element is duration
            else:
                duration_map[plan_name] = 30  # Default fallback
        
        return duration_map
    except (FileNotFoundError, json.JSONDecodeError):
        return {"1 Months": 30, "3 Months": 90, "6 Months": 180, "12 Months": 365}