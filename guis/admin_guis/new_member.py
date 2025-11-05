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
        return [(t["username"], t.get("name") or f"{t.get('f_name', '')} {t.get('l_name', '')}".strip()) for t in trainers]
    except Exception:
        return []

def on_new_member(root, admin):
    text_label = ttk.Label(root, text="New Member", font=("Arial", 24))
    text_label.pack(pady=20)

    # Khung chính
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=30, pady=20)

    # Khung cho form, sử dụng grid
    form_frame = ttk.Frame(main_frame)
    form_frame.pack(pady=10)

    entries = {}

    # --- Bố cục .grid() cho form ---
    # Cấu hình cột để co giãn
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=2)
    
    # Định nghĩa các trường
    fields = [
        ("First Name", "f_name"), ("Last Name", "l_name"),
        ("Phone", "phone"), ("Address", "address"),
        ("Email", "email"), ("Username", "username")
    ]
    
    # Tạo các trường entry
    for i, (label_text, key) in enumerate(fields):
        label = ttk.Label(form_frame, text=label_text, font=("Arial", 11))
        label.grid(row=i, column=0, sticky="w", padx=10, pady=8)
        
        entry = ttk.Entry(form_frame, font=("Arial", 11), width=30)
        entry.grid(row=i, column=1, sticky="w", padx=10, pady=8)
        entries[key] = entry

    row_index = len(fields)

    # Gender
    label = ttk.Label(form_frame, text="Gender", font=("Arial", 11))
    label.grid(row=row_index, column=0, sticky="w", padx=10, pady=8)
    
    gender_var = tk.StringVar(value="male")
    gender_frame = ttk.Frame(form_frame)
    gender_frame.grid(row=row_index, column=1, sticky="w", padx=10, pady=8)
    
    male_radio = ttk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="male")
    male_radio.pack(side="left", padx=(0, 20))
    female_radio = ttk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="female")
    female_radio.pack(side="left")
    entries["gender"] = gender_var
    row_index += 1

    # Date of Birth
    label = ttk.Label(form_frame, text="Date of Birth", font=("Arial", 11))
    label.grid(row=row_index, column=0, sticky="w", padx=10, pady=8)
    dob_calendar = DateEntry(form_frame, width=28, background='darkblue', foreground='white', 
                           borderwidth=2, date_pattern='yyyy-mm-dd', maxdate=datetime.now(),
                           year=2000, month=1, day=1)
    dob_calendar.grid(row=row_index, column=1, sticky="w", padx=10, pady=8)
    entries["date_of_birth"] = dob_calendar
    row_index += 1

    # Joined Date
    label = ttk.Label(form_frame, text="Joined Date", font=("Arial", 11))
    label.grid(row=row_index, column=0, sticky="w", padx=10, pady=8)
    joined_calendar = DateEntry(form_frame, width=28, background='darkblue', foreground='white', 
                              borderwidth=2, date_pattern='yyyy-mm-dd', maxdate=datetime.now(),
                              year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    joined_calendar.grid(row=row_index, column=1, sticky="w", padx=10, pady=8)
    entries["joined_date"] = joined_calendar
    row_index += 1

    # Membership
    label = ttk.Label(form_frame, text="Membership", font=("Arial", 11))
    label.grid(row=row_index, column=0, sticky="w", padx=10, pady=8)
    subscription_data = read_subscription_info()
    membership_options = list(subscription_data.keys()) if subscription_data else ["1 Months"]
    membership_var = tk.StringVar(value=membership_options[0] if membership_options else "")
    membership_dropdown = ttk.Combobox(form_frame, textvariable=membership_var, values=membership_options, 
                                      state="readonly", width=27, font=("Arial", 10))
    membership_dropdown.grid(row=row_index, column=1, sticky="w", padx=10, pady=8)
    entries["membership"] = membership_var
    row_index += 1

    # Trainer
    label = ttk.Label(form_frame, text="Trainer Username", font=("Arial", 11))
    label.grid(row=row_index, column=0, sticky="w", padx=10, pady=8)
    trainer_list = load_trainers()
    trainer_usernames = [t[0] for t in trainer_list]
    trainer_var = tk.StringVar(value=trainer_usernames[0] if trainer_usernames else "")
    trainer_dropdown = ttk.Combobox(form_frame, textvariable=trainer_var, values=trainer_usernames, 
                                    state="readonly", width=27, font=("Arial", 10))
    trainer_dropdown.grid(row=row_index, column=1, sticky="w", padx=10, pady=8)
    entries["trainer_username"] = trainer_var
    row_index += 1

    # Subscription Expiry
    label = ttk.Label(form_frame, text="Subscription Expiry", font=("Arial", 11))
    label.grid(row=row_index, column=0, sticky="w", padx=10, pady=8)
    expiry_calendar = DateEntry(form_frame, width=28, background='darkblue', foreground='white', 
                               borderwidth=2, date_pattern='yyyy-mm-dd')
    expiry_calendar.grid(row=row_index, column=1, sticky="w", padx=10, pady=8)
    entries["subscription_expiry"] = expiry_calendar
    row_index += 1

    def update_expiry_date(*args):
        try:
            membership = membership_var.get()
            joined_date = joined_calendar.get_date()
            duration_map = read_subscription_info()
            days = duration_map.get(membership, 30) # Mặc định 30 ngày nếu không tìm thấy
            expiry_date = joined_date + timedelta(days=days)
            expiry_calendar.set_date(expiry_date)
        except Exception as e:
            print(f"Error updating expiry date: {e}")

    membership_var.trace('w', update_expiry_date)
    joined_calendar.bind("<<DateEntrySelected>>", update_expiry_date)
    
    # Khởi tạo giá trị
    joined_calendar.set_date(datetime.now())
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
        
        values["name"] = f"{values.get('f_name', '')} {values.get('l_name', '')}".strip()
        values["attendance_days"] = []
        values["workout_days"] = []
        
        if any(v == "" for k, v in values.items() if k not in ["attendance_days", "workout_days"]):
            messagebox.showerror("Error", "All fields must be filled!")
            return
            
        if admin.new_member(values):
            messagebox.showinfo("Success", "Member added successfully!")
            for key, entry in entries.items():
                if key == "gender": entry.set("male")
                elif key in ["date_of_birth"]: entry.set_date(datetime(2000, 1, 1))
                elif key in ["joined_date"]: entry.set_date(datetime.now())
                elif key == "membership": entry.set(membership_options[0] if membership_options else "")
                elif key == "trainer_username": entry.set(trainer_usernames[0] if trainer_usernames else "")
                elif hasattr(entry, 'delete'): entry.delete(0, tk.END)
            update_expiry_date()
        else:
            messagebox.showerror("Error", "Failed to add member. Please try again.")

    # Khung nút
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(side="bottom", pady=20)

    submit_btn = ttk.Button(button_frame, text="Submit", command=submit, style="Success.TButton")
    submit_btn.pack(side="left", padx=10)

    back_btn = ttk.Button(button_frame, text="Back to Menu", command=root.destroy, style="Primary.TButton")
    back_btn.pack(side="left", padx=10)

def read_subscription_info():
    try:
        with open("data/subscription_info.json", 'r') as f:
            subscription_data = json.load(f)
        duration_map = {plan: data[0] for plan, data in subscription_data.items() if isinstance(data, list) and len(data) > 0}
        return duration_map
    except (FileNotFoundError, json.JSONDecodeError):
        return {"1 Months": 30, "3 Months": 90, "6 Months": 180, "12 Months": 365}