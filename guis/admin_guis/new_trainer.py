import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
from models.admin import Admin

def on_new_trainer(root, admin):
    text_label = ttk.Label(root, text="New Trainer", font=("Arial", 24))
    text_label.pack(pady=20)

    # Khung chính
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=30, pady=20)
    
    # Khung cho form, sử dụng grid
    form_frame = ttk.Frame(main_frame)
    form_frame.pack(pady=10)

    entries = {}

    # --- Bố cục .grid() cho form ---
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=2)
    
    fields = [
        ("First Name", "f_name"), ("Last Name", "l_name"),
        ("Phone", "phone"), ("Address", "address"),
        ("Email", "email"), ("Username", "username"),
        ("Height (cm)", "height"), ("Weight (kg)", "weight"),
        ("Trainer ID", "trainer_id")
    ]

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

    def submit():
        values = {}
        for key, entry in entries.items():
            if key == "gender":
                values[key] = entry.get()
            elif key in ["date_of_birth", "joined_date"]:
                values[key] = entry.get_date().strftime('%Y-%m-%d')
            else:
                values[key] = entry.get()
                
        if any(v == "" for v in values.values()):
            messagebox.showerror("Error", "All fields must be filled!")
            return
            
        if admin.new_trainer(values):
            messagebox.showinfo("Success", "Trainer added successfully!")
            for key, entry in entries.items():
                if key == "gender": entry.set("male")
                elif key in ["date_of_birth"]: entry.set_date(datetime(2000, 1, 1))
                elif key in ["joined_date"]: entry.set_date(datetime.now())
                elif hasattr(entry, 'delete'): entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to add trainer. Please try again.")

    # Khung nút
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(side="bottom", pady=20)

    submit_btn = ttk.Button(button_frame, text="Submit", command=submit, style="Success.TButton")
    submit_btn.pack(side="left", padx=10)

    back_btn = ttk.Button(button_frame, text="Back to Menu", command=root.destroy, style="Primary.TButton")
    back_btn.pack(side="left", padx=10)