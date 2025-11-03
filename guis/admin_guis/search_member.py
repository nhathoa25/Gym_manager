import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import json

def load_trainers():
    try:
        with open("data/trainer_info.json", "r", encoding="utf-8") as f:
            trainers = json.load(f)
        return [(t["username"], t.get("name") or f"{t.get('f_name', '')} {t.get('l_name', '')}".strip()) for t in trainers]
    except Exception:
        return []

def on_search_member(root, admin):
    root.title("Search and Edit Member")
    text_label = tk.Label(root, text="Search and Edit Member", font=("Arial", 24), bg=root["bg"])
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

    # Create Treeview for search results
    columns = ("Username", "First Name", "Last Name", "Email", "Phone", "Membership", "Expiry")
    tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=8)
    
    # Set column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Edit frame (initially hidden)
    edit_frame = tk.Frame(main_frame, bg=root["bg"])
    
    # Variables for edit form
    edit_entries = {}
    
    def load_all_members():
        """Load and display all members"""
        # Clear previous results
        for item in tree.get_children():
            tree.delete(item)
        
        # Get all members (empty search term returns all members)
        all_members = admin.search_members("")
        
        for member in all_members:
            tree.insert("", "end", values=(
                member.get('username', 'N/A'),
                member.get('f_name', 'N/A'),
                member.get('l_name', 'N/A'),
                member.get('email', 'N/A'),
                member.get('phone', 'N/A'),
                member.get('membership', 'N/A'),
                member.get('subscription_expiry', 'N/A')
            ))
    
    def search_members():
        """Search members by name using admin method"""
        search_term = search_var.get().strip()
        
        # Clear previous results
        for item in tree.get_children():
            tree.delete(item)
        
        if not search_term:
            # If no search term, show all members
            load_all_members()
            return
        
        # Use admin's search method
        found_members = admin.search_members(search_term)
        
        for member in found_members:
            tree.insert("", "end", values=(
                member.get('username', 'N/A'),
                member.get('f_name', 'N/A'),
                member.get('l_name', 'N/A'),
                member.get('email', 'N/A'),
                member.get('phone', 'N/A'),
                member.get('membership', 'N/A'),
                member.get('subscription_expiry', 'N/A')
            ))
        
        if not found_members:
            messagebox.showinfo("No Results", f"No members found matching '{search_term}'")

    def on_select_member(event):
        """Handle member selection for editing"""
        selection = tree.selection()
        if not selection:
            return
        
        # Get selected member data
        selected_username = tree.item(selection[0])['values'][0]
        all_members = admin.search_members("")  # Get all members to find the selected one
        selected_member = None
        
        for member in all_members:
            if member.get('username') == selected_username:
                selected_member = member
                break
        
        if selected_member:
            show_edit_form(selected_member)

    def show_edit_form(member):
        """Show the edit form with member data"""
        # Clear previous edit frame
        for widget in edit_frame.winfo_children():
            widget.destroy()
        
        edit_frame.pack(fill="both", expand=True, pady=10)
        
        # Title for edit section
       
        
        # Create form fields
        fields = [
            ("First Name", "f_name", "entry"),
            ("Last Name", "l_name", "entry"),
            ("Phone", "phone", "entry"),
            ("Address", "address", "entry"),
            ("Email", "email", "entry"),
        ]
        
        entries = {}
        start_y = 0.01
        step_y = 0.08
        
        # Create regular entry fields
        for i, (label_text, key, field_type) in enumerate(fields):
            y = start_y + i * step_y
            label = tk.Label(edit_frame, text=label_text, bg=root["bg"], font=("Arial", 10))
            label.place(relx=0.1, rely=y, anchor="w")
            
            if field_type == "entry":
                entry = tk.Entry(edit_frame, font=("Arial", 10))
                entry.insert(0, member.get(key, ""))
                entry.place(relx=0.4, rely=y, anchor="w", width=200)
                entries[key] = entry
        
        # Gender selection
        gender_label = tk.Label(edit_frame, text="Gender", bg=root["bg"], font=("Arial", 10))
        gender_label.place(relx=0.1, rely=start_y + len(fields) * step_y, anchor="w")
        
        gender_var = tk.StringVar(value=member.get('gender', 'male'))
        gender_frame = tk.Frame(edit_frame, bg=root["bg"])
        gender_frame.place(relx=0.4, rely=start_y + len(fields) * step_y, anchor="w")
        
        male_radio = tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="male", bg=root["bg"])
        male_radio.pack(side="left", padx=(0, 20))
        female_radio = tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="female", bg=root["bg"])
        female_radio.pack(side="left")
        entries["gender"] = gender_var
        
        # Date of Birth calendar
        dob_label = tk.Label(edit_frame, text="Date of Birth", bg=root["bg"], font=("Arial", 10))
        dob_label.place(relx=0.1, rely=start_y + (len(fields) + 1) * step_y, anchor="w")
        
        try:
            dob_date = datetime.strptime(member.get('date_of_birth', '2000-01-01'), '%Y-%m-%d')
        except:
            dob_date = datetime(2000, 1, 1)
            
        dob_calendar = DateEntry(edit_frame, width=20, background='darkblue', foreground='white', 
                               borderwidth=2, date_pattern='yyyy-mm-dd', maxdate=datetime.now(),
                               year=dob_date.year, month=dob_date.month, day=dob_date.day,
                               firstweekday='sunday', showweeknumbers=False, selectmode='day')
        dob_calendar.place(relx=0.4, rely=start_y + (len(fields) + 1) * step_y, anchor="w")
        entries["date_of_birth"] = dob_calendar
        
        # Joined Date calendar
        joined_label = tk.Label(edit_frame, text="Joined Date", bg=root["bg"], font=("Arial", 10))
        joined_label.place(relx=0.1, rely=start_y + (len(fields) + 2) * step_y, anchor="w")
        
        try:
            joined_date = datetime.strptime(member.get('joined_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
        except:
            joined_date = datetime.now()
            
        joined_calendar = DateEntry(edit_frame, width=20, background='darkblue', foreground='white', 
                                  borderwidth=2, date_pattern='yyyy-mm-dd', maxdate=datetime.now(),
                                  year=joined_date.year, month=joined_date.month, day=joined_date.day,
                                  firstweekday='sunday', showweeknumbers=False, selectmode='day')
        joined_calendar.place(relx=0.4, rely=start_y + (len(fields) + 2) * step_y, anchor="w")
        entries["joined_date"] = joined_calendar
        
        # Membership dropdown
        membership_label = tk.Label(edit_frame, text="Membership", bg=root["bg"], font=("Arial", 10))
        membership_label.place(relx=0.1, rely=start_y + (len(fields) + 3) * step_y, anchor="w")
        
        membership_options = ["1 Months", "3 Months", "6 Months", "12 Months", "36 Months", "Lifetime"]
        membership_var = tk.StringVar(value=member.get('membership', membership_options[0]))
        membership_dropdown = ttk.Combobox(edit_frame, textvariable=membership_var, values=membership_options, 
                                          state="readonly", width=17)
        membership_dropdown.place(relx=0.4, rely=start_y + (len(fields) + 3) * step_y, anchor="w")
        entries["membership"] = membership_var
        
        # Trainer selection
        trainer_label = tk.Label(edit_frame, text="Trainer Username", bg=root["bg"], font=("Arial", 10))
        trainer_label.place(relx=0.1, rely=start_y + (len(fields) + 4) * step_y, anchor="w")
        trainer_list = load_trainers()
        trainer_usernames = [t[0] for t in trainer_list]
        trainer_display = [f"{t[1]} ({t[0]})" for t in trainer_list]
        trainer_var = tk.StringVar(value=member.get('trainer_username', trainer_usernames[0] if trainer_usernames else ""))
        trainer_dropdown = ttk.Combobox(edit_frame, textvariable=trainer_var, values=trainer_usernames, state="readonly", width=17)
        trainer_dropdown.place(relx=0.4, rely=start_y + (len(fields) + 4) * step_y, anchor="w")
        entries["trainer_username"] = trainer_var
        
        # Subscription expiry calendar
        expiry_label = tk.Label(edit_frame, text="Subscription Expiry", bg=root["bg"], font=("Arial", 10))
        expiry_label.place(relx=0.1, rely=start_y + (len(fields) + 5) * step_y, anchor="w")
        
        try:
            expiry_date = datetime.strptime(member.get('subscription_expiry', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
        except:
            expiry_date = datetime.now()
            
        expiry_calendar = DateEntry(edit_frame, width=20, background='darkblue', foreground='white', 
                                   borderwidth=2, date_pattern='yyyy-mm-dd',
                                   year=expiry_date.year, month=expiry_date.month, day=expiry_date.day,
                                   firstweekday='sunday', showweeknumbers=False, selectmode='day')
        expiry_calendar.place(relx=0.4, rely=start_y + (len(fields) + 5) * step_y, anchor="w")
        entries["subscription_expiry"] = expiry_calendar
        
        def update_expiry_date(*args):
            """Update subscription expiry date based on membership selection"""
            membership = membership_var.get()
            joined_date = joined_calendar.get_date()
            
            duration_map = {
                "1 Months": 30,
                "3 Months": 90,
                "6 Months": 180,
                "12 Months": 365,
                "36 Months": 365*3,
                "Lifetime": 365*100
            }
            days = duration_map.get(membership, 30)
            expiry_date = joined_date + timedelta(days=days)
            expiry_calendar.set_date(expiry_date)
        
        membership_var.trace('w', update_expiry_date)
        
        def save_changes():
            """Save the edited member information using admin method"""
            values = {}
            for key, entry in entries.items():
                if key == "gender":
                    values[key] = entry.get()
                elif key in ["date_of_birth", "joined_date", "subscription_expiry"]:
                    values[key] = entry.get_date().strftime('%Y-%m-%d')
                else:
                    values[key] = entry.get()
            
            if any(v == "" for v in values.values()):
                messagebox.showerror("Error", "All fields must be filled!")
                return
            
            # Use admin's update method
            if admin.update_member(member.get('username'), values):
                messagebox.showinfo("Success", "Member information updated successfully!")
                # Refresh member list
                load_all_members()
                # Hide edit form
                edit_frame.pack_forget()
            else:
                messagebox.showerror("Error", "Failed to update member information!")

        def delete_member():
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete member '{member.get('username')}'?")
            if not confirm:
                return
            if admin.delete_member(member.get('username')):
                messagebox.showinfo("Success", "Member deleted successfully!")
                load_all_members()
                edit_frame.pack_forget()
            else:
                messagebox.showerror("Error", "Failed to delete member!")

        # Button frame for Save, Delete, and Back buttons
        button_frame = tk.Frame(edit_frame, bg=root["bg"])
        button_frame.place(relx=0.8, rely=0.8, anchor="n")

        save_btn = tk.Button(button_frame, text="Save Changes", command=save_changes,
                            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                            relief="raised", bd=2)
        save_btn.pack(side="left", padx=10)

        delete_btn = tk.Button(button_frame, text="Delete Member", command=delete_member,
                              font=("Arial", 12, "bold"), bg="#f44336", fg="white",
                              relief="raised", bd=2)
        delete_btn.pack(side="left", padx=10)

        def cancel_edit():
            edit_frame.pack_forget()

        cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel_edit,
                              font=("Arial", 12, "bold"), bg="#888888", fg="white",
                              relief="raised", bd=2)
        cancel_btn.pack(side="left", padx=10)

    # Search button
    search_btn = tk.Button(search_frame, text="Search", command=search_members,
                          font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
                          relief="raised", bd=2)
    search_btn.pack(side="left", padx=10)
    
    # Show all members button
    show_all_btn = tk.Button(search_frame, text="Show All Members", command=load_all_members,
                             font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                             relief="raised", bd=2)
    show_all_btn.pack(side="left", padx=10)
    
    # Bind tree selection event
    tree.bind("<<TreeviewSelect>>", on_select_member)
    
    # Load all members when the window opens
    load_all_members()
    
    # Back to menu button
    def back_to_menu():
        root.destroy()
    
    back_btn = tk.Button(main_frame, text="Back to Menu", command=back_to_menu,
                        font=("Arial", 14, "bold"), bg="#2196F3", fg="white",
                        relief="raised", bd=2)
    back_btn.pack(pady=1)
