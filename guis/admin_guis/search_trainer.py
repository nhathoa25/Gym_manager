import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import json
import os

def load_all_trainers():
    if not os.path.exists("data/trainer_info.json"):
        return []
    with open("data/trainer_info.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_all_trainers(trainers):
    with open("data/trainer_info.json", "w", encoding="utf-8") as f:
        json.dump(trainers, f, indent=4, ensure_ascii=False)

def on_search_trainer(root, admin):
    root.title("Search and Edit Trainer")
    text_label = tk.Label(root, text="Search and Edit Trainer", font=("Arial", 24), bg=root["bg"])
    text_label.pack(pady=20)

    main_frame = tk.Frame(root, bg=root["bg"])
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Search frame
    search_frame = tk.Frame(main_frame, bg=root["bg"])
    search_frame.pack(fill="x", pady=10)

    search_label = tk.Label(search_frame, text="Search by Name:", font=("Arial", 12), bg=root["bg"])
    search_label.pack(side="left", padx=(0, 10))

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 12), width=30)
    search_entry.pack(side="left", padx=(0, 10))

    # Results frame
    results_frame = tk.Frame(main_frame, bg=root["bg"])
    results_frame.pack(fill="both", expand=True, pady=10)

    # Treeview for trainers
    columns = ("Username", "First Name", "Last Name", "Email", "Phone", "Trainer ID", "Height", "Weight")
    tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=6)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110)
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="x", expand=False)
    scrollbar.pack(side="right", fill="y")
    results_frame.pack_propagate(False)
    results_frame.configure(height=150)

    # Edit frame (initially hidden)
    edit_frame = tk.Frame(main_frame, bg=root["bg"])
    edit_entries = {}

    def refresh_trainer_list(trainers):
        for item in tree.get_children():
            tree.delete(item)
        for trainer in trainers:
            tree.insert("", "end", values=(
                trainer.get('username', ''),
                trainer.get('f_name', ''),
                trainer.get('l_name', ''),
                trainer.get('email', ''),
                trainer.get('phone', ''),
                trainer.get('trainer_id', ''),
                trainer.get('height', ''),
                trainer.get('weight', '')
            ))

    def search_trainers():
        search_term = search_var.get().strip()
        found = admin.search_trainer(search_term)
        refresh_trainer_list(found)
        if not found:
            messagebox.showinfo("No Results", f"No trainers found matching '{search_term}'")

    def on_select_trainer(event):
        selection = tree.selection()
        if not selection:
            return
        selected_username = tree.item(selection[0])['values'][0]
        all_trainers = load_all_trainers()
        selected_trainer = None
        for t in all_trainers:
            if t.get('username') == selected_username:
                selected_trainer = t
                break
        if selected_trainer:
            show_edit_form(selected_trainer)

    def show_edit_form(trainer):
        for widget in edit_frame.winfo_children():
            widget.destroy()
        edit_frame.pack(fill="both", expand=True, pady=10)

        fields = [
            ("First Name", "f_name"),
            ("Last Name", "l_name"),
            ("Phone", "phone"),
            ("Address", "address"),
            ("Email", "email"),
            ("Username", "username"),
            ("Gender", "gender"),
            ("Date of Birth", "date_of_birth"),
            ("Joined Date", "joined_date"),
            ("Height", "height"),
            ("Weight", "weight"),
            ("Trainer ID", "trainer_id"),
            ("Member Usernames", "member_username")
        ]
        entries = {}
        y = 0.01
        step_y = 0.07
        for label_text, key in fields:
            label = tk.Label(edit_frame, text=label_text, bg=root["bg"], font=("Arial", 10))
            label.place(relx=0.1, rely=y, anchor="w")
            if key in ["date_of_birth", "joined_date"]:
                try:
                    date_val = datetime.strptime(trainer.get(key, '2000-01-01'), '%Y-%m-%d')
                except:
                    date_val = datetime(2000, 1, 1)
                cal = DateEntry(edit_frame, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', year=date_val.year, month=date_val.month, day=date_val.day, firstweekday='sunday', showweeknumbers=False, selectmode='day')
                cal.place(relx=0.4, rely=y, anchor="w")
                entries[key] = cal
            elif key == "gender":
                gender_var = tk.StringVar(value=trainer.get('gender', 'male'))
                gender_frame = tk.Frame(edit_frame, bg=root["bg"])
                gender_frame.place(relx=0.4, rely=y, anchor="w")
                male_radio = tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="male", bg=root["bg"])
                male_radio.pack(side="left", padx=(0, 20))
                female_radio = tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="female", bg=root["bg"])
                female_radio.pack(side="left")
                entries[key] = gender_var
            elif key == "member_username":
                # Always show as comma+space separated string
                entry = tk.Entry(edit_frame, font=("Arial", 10), width=40)
                entry.insert(0, ', '.join(trainer.get('member_username', [])))
                entry.place(relx=0.4, rely=y, anchor="w")
                entries[key] = entry
            else:
                entry = tk.Entry(edit_frame, font=("Arial", 10), width=30)
                entry.insert(0, str(trainer.get(key, "")))
                entry.place(relx=0.4, rely=y, anchor="w")
                entries[key] = entry
            y += step_y
        def save_changes():
            all_trainers = load_all_trainers()
            for t in all_trainers:
                if t.get('username') == trainer.get('username'):
                    for label_text, key in fields:
                        if key in ["date_of_birth", "joined_date"]:
                            t[key] = entries[key].get_date().strftime('%Y-%m-%d')
                        elif key == "gender":
                            t[key] = entries[key].get()
                        elif key == "member_username":
                            # Always split by ', ' and return list
                            t[key] = [u.strip() for u in entries[key].get().split(',') if u.strip()]
                        else:
                            t[key] = entries[key].get()
                    break
            save_all_trainers(all_trainers)
            messagebox.showinfo("Success", "Trainer information updated successfully!")
            refresh_trainer_list(all_trainers)
            edit_frame.pack_forget()
        def delete_trainer():
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete trainer '{trainer.get('username')}'?")
            if not confirm:
                return
            all_trainers = load_all_trainers()
            all_trainers = [t for t in all_trainers if t.get('username') != trainer.get('username')]
            save_all_trainers(all_trainers)
            messagebox.showinfo("Success", "Trainer deleted successfully!")
            refresh_trainer_list(all_trainers)
            edit_frame.pack_forget()
        def cancel_edit():
            edit_frame.pack_forget()
        # Always show buttons at the bottom of the edit frame
        button_frame = tk.Frame(edit_frame, bg=root["bg"])
        button_frame.place(relx=0.8, rely=0.8, anchor="n")
        save_btn = tk.Button(button_frame, text="Save Changes", command=save_changes, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="raised", bd=2)
        save_btn.pack(side="left", padx=10)
        delete_btn = tk.Button(button_frame, text="Delete Trainer", command=delete_trainer, font=("Arial", 12, "bold"), bg="#f44336", fg="white", relief="raised", bd=2)
        delete_btn.pack(side="left", padx=10)
        cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel_edit, font=("Arial", 12, "bold"), bg="#888888", fg="white", relief="raised", bd=2)
        cancel_btn.pack(side="left", padx=10)
    tree.bind("<<TreeviewSelect>>", on_select_trainer)
    def show_all():
        refresh_trainer_list(admin.search_trainer(""))
    search_btn = tk.Button(search_frame, text="Search", command=search_trainers, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="raised", bd=2)
    search_btn.pack(side="left", padx=10)
    show_all_btn = tk.Button(search_frame, text="Show All Trainers", command=show_all, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="raised", bd=2)
    show_all_btn.pack(side="left", padx=10)
    show_all()
    def back_to_menu():
        root.destroy()
    back_btn = tk.Button(main_frame, text="Back to Menu", command=back_to_menu, font=("Arial", 14, "bold"), bg="#2196F3", fg="white", relief="raised", bd=2)
    back_btn.pack(pady=1) 