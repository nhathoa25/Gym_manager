import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
from models.admin import Admin


def on_new_trainer(root, admin):
    text_label = tk.Label(root, text="New trainer", font=("Arial", 24), bg=root["bg"])
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
        ("Height (cm)", "height", "entry"),
        ("Weight (kg)", "weight", "entry"),
        ("Trainer ID", "trainer_id", "entry"),
    ]

    entries = {}
    start_y = 0.05
    step_y = 0.07

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
        # Create Admin instance and add trainer
        if admin.new_trainer(values):
            messagebox.showinfo("Success", "Trainer added successfully!")
            # Clear all fields after successful submission
            for key, entry in entries.items():
                if key == "gender":
                    entry.set("male")
                elif key in ["date_of_birth", "joined_date"]:
                    entry.set_date(datetime.now())
                else:
                    entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to add trainer. Please try again.")

    # Button frame for Submit and Back buttons
    button_frame = tk.Frame(main_frame, bg=root["bg"])
    button_frame.place(relx=0.5, rely=start_y + (len(fields) + 3.5) * step_y, anchor="n")

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

