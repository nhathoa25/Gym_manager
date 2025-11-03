import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import json
import os

def load_all_members():
    if not os.path.exists("data/member_info.json"):
        return []
    with open("data/member_info.json", "r", encoding="utf-8") as f:
        return json.load(f)

def export_attendance_to_csv():
    members = load_all_members()
    rows = []
    for m in members:
        username = m.get("username", "")
        name = m.get("name") or f"{m.get('f_name', '')} {m.get('l_name', '')}".strip()
        for day in m.get("attendance_days", []):
            rows.append([username, name, day])
    if not rows:
        messagebox.showinfo("No Data", "No attendance data to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save Attendance Report")
    if not file_path:
        return
    import csv
    with open(file_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Username", "Name", "Attendance Day"])
        writer.writerows(rows)
    messagebox.showinfo("Success", f"Attendance report saved to {file_path}")

def on_add_attendance(root, trainer):
    root.title("Add Attendance Day & Export Report")
    text_label = tk.Label(root, text="Add Attendance Day & Export Report", font=("Arial", 24), bg=root["bg"])
    text_label.pack(pady=20)

    main_frame = tk.Frame(root, bg=root["bg"])
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Only show members assigned to this trainer
    all_members = load_all_members()
    trainer_member_usernames = set(getattr(trainer, 'member_username', []))
    # If not set, try to get from trainer_info.json
    if not trainer_member_usernames:
        try:
            with open("data/trainer_info.json", "r", encoding="utf-8") as f:
                trainers = json.load(f)
            for t in trainers:
                if t.get("username") == getattr(trainer, "username", None):
                    trainer_member_usernames = set(t.get("member_username", []))
                    break
        except Exception:
            pass
    filtered_members = [m for m in all_members if m.get("username") in trainer_member_usernames]
    member_options = [(m.get("username", ""), m.get("name") or f"{m.get('f_name', '')} {m.get('l_name', '')}".strip()) for m in filtered_members]
    member_usernames = [u for u, n in member_options]
    member_display = [f"{n} ({u})" for u, n in member_options]
    member_label = tk.Label(main_frame, text="Select Member:", font=("Arial", 12), bg=root["bg"])
    member_label.pack(pady=(0, 5))
    member_var = tk.StringVar(value=member_usernames[0] if member_usernames else "")
    member_dropdown = ttk.Combobox(main_frame, textvariable=member_var, values=member_usernames, state="readonly", width=30)
    member_dropdown.pack(pady=(0, 15))

    # Date picker
    date_label = tk.Label(main_frame, text="Select Attendance Date:", font=("Arial", 12), bg=root["bg"])
    date_label.pack(pady=(0, 5))
    date_entry = DateEntry(main_frame, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, firstweekday='sunday', showweeknumbers=False, selectmode='day')
    date_entry.pack(pady=(0, 15))

    def add_attendance():
        username = member_var.get()
        date_str = date_entry.get_date().strftime('%Y-%m-%d')
        if not username:
            messagebox.showerror("Error", "Please select a member.")
            return
        if trainer.add_attendance_day(username, date_str):
            messagebox.showinfo("Success", f"Added attendance for {username} on {date_str}")
        else:
            messagebox.showerror("Error", "Failed to add attendance day!")

    add_btn = tk.Button(main_frame, text="Add Attendance", command=add_attendance, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="raised", bd=2)
    add_btn.pack(pady=10)

    export_btn = tk.Button(main_frame, text="Export Attendance Report to CSV", command=export_attendance_to_csv, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="raised", bd=2)
    export_btn.pack(pady=10)

    def back_to_menu():
        root.destroy()
    back_btn = tk.Button(main_frame, text="Back to Menu", command=back_to_menu, font=("Arial", 14, "bold"), bg="#2196F3", fg="white", relief="raised", bd=2)
    back_btn.pack(pady=10)
