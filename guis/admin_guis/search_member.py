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

def read_subscription_info():
    """Đọc thông tin gói tập để lấy danh sách"""
    try:
        with open("data/subscription_info.json", 'r') as f:
            subscription_data = json.load(f)
        return list(subscription_data.keys())
    except (FileNotFoundError, json.JSONDecodeError):
        return ["1 Months", "3 Months", "6 Months", "12 Months"]

def on_search_member(root, admin):
    root.title("Search and Edit Member")
    
    text_label = ttk.Label(root, text="Search and Edit Member", font=("Arial", 24))
    text_label.pack(pady=20)

    main_frame = ttk.Frame(root)
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Search frame
    search_frame = ttk.Frame(main_frame)
    search_frame.pack(fill="x", pady=10)

    search_label = ttk.Label(search_frame, text="Search by Name:", font=("Arial", 12))
    search_label.pack(side="left", padx=(0, 10))

    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var, font=("Arial", 12), width=30)
    search_entry.pack(side="left", padx=(0, 10))

    # Results frame (SẼ ĐƯỢC ẨN/HIỆN)
    results_frame = ttk.Frame(main_frame)
    results_frame.pack(fill="both", expand=True, pady=10)

    columns = ("Username", "First Name", "Last Name", "Email", "Phone", "Membership", "Expiry")
    tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=8)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # === TỐI ƯU HÓA: Tạo form chỉnh sửa 1 LẦN (ban đầu ẩn) ===
    edit_frame = ttk.Frame(main_frame) 
    entries = {} 

    def cancel_edit():
        """SỬA LỖI: Ẩn form edit VÀ hiện lại bảng results"""
        edit_frame.pack_forget()
        results_frame.pack(fill="both", expand=True, pady=10) # Hiện lại

    def create_edit_form_structure():
        """Tạo cấu trúc form 1 lần, lưu widget vào 'entries'"""
        
        form_grid = ttk.Frame(edit_frame)
        form_grid.pack(fill="x", expand=True)
        
        form_grid.columnconfigure(1, weight=1) 
        
        fields = [
            ("First Name", "f_name"), ("Last Name", "l_name"),
            ("Phone", "phone"), ("Address", "address"),
            ("Email", "email")
        ]
        
        row_index = 0
        for label_text, key in fields:
            label = ttk.Label(form_grid, text=label_text, font=("Arial", 11))
            label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
            
            entry = ttk.Entry(form_grid, font=("Arial", 11))
            entry.grid(row=row_index, column=1, sticky="ew", padx=10, pady=5)
            entries[key] = entry
            row_index += 1
        
        # Gender
        label = ttk.Label(form_grid, text="Gender", font=("Arial", 11))
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
        gender_var = tk.StringVar()
        gender_frame = ttk.Frame(form_grid)
        gender_frame.grid(row=row_index, column=1, sticky="w", padx=10, pady=5) # sticky 'w'
        male_radio = ttk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="male")
        male_radio.pack(side="left", padx=(0, 20))
        female_radio = ttk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="female")
        female_radio.pack(side="left")
        entries["gender"] = gender_var
        row_index += 1
        
        # DOB
        label = ttk.Label(form_grid, text="Date of Birth", font=("Arial", 11))
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
        dob_calendar = DateEntry(form_grid, background='darkblue', foreground='white', 
                               borderwidth=2, date_pattern='yyyy-mm-dd', maxdate=datetime.now())
        dob_calendar.grid(row=row_index, column=1, sticky="ew", padx=10, pady=5)
        entries["date_of_birth"] = dob_calendar
        row_index += 1
        
        # Joined Date
        label = ttk.Label(form_grid, text="Joined Date", font=("Arial", 11))
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
        joined_calendar = DateEntry(form_grid, background='darkblue', foreground='white', 
                                  borderwidth=2, date_pattern='yyyy-mm-dd', maxdate=datetime.now())
        joined_calendar.grid(row=row_index, column=1, sticky="ew", padx=10, pady=5)
        entries["joined_date"] = joined_calendar
        row_index += 1
        
        # Membership
        label = ttk.Label(form_grid, text="Membership", font=("Arial", 11))
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
        membership_options = read_subscription_info()
        membership_var = tk.StringVar()
        membership_dropdown = ttk.Combobox(form_grid, textvariable=membership_var, values=membership_options, 
                                          state="readonly", font=("Arial", 10))
        membership_dropdown.grid(row=row_index, column=1, sticky="ew", padx=10, pady=5)
        entries["membership"] = membership_var
        row_index += 1
        
        # Trainer
        label = ttk.Label(form_grid, text="Trainer Username", font=("Arial", 11))
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
        trainer_list = load_trainers()
        trainer_usernames = [t[0] for t in trainer_list]
        trainer_var = tk.StringVar()
        trainer_dropdown = ttk.Combobox(form_grid, textvariable=trainer_var, values=trainer_usernames, 
                                        state="readonly", font=("Arial", 10))
        trainer_dropdown.grid(row=row_index, column=1, sticky="ew", padx=10, pady=5)
        entries["trainer_username"] = trainer_var
        row_index += 1
        
        # Expiry
        label = ttk.Label(form_grid, text="Subscription Expiry", font=("Arial", 11))
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
        expiry_calendar = DateEntry(form_grid, background='darkblue', foreground='white', 
                                   borderwidth=2, date_pattern='yyyy-mm-dd')
        expiry_calendar.grid(row=row_index, column=1, sticky="ew", padx=10, pady=5)
        entries["subscription_expiry"] = expiry_calendar
        row_index += 1
        
        def update_expiry_date(*args):
            try:
                membership = membership_var.get()
                joined_date = joined_calendar.get_date()
                sub_map = {}
                try:
                    with open("data/subscription_info.json", 'r') as f:
                        data = json.load(f)
                        sub_map = {plan: details[0] for plan, details in data.items()}
                except:
                    sub_map = { "1 Months": 30, "3 Months": 90, "6 Months": 180, "12 Months": 365, "36 Months": 365*3, "Lifetime": 365*100 }

                days = sub_map.get(membership, 30)
                expiry_date = joined_date + timedelta(days=days)
                expiry_calendar.set_date(expiry_date)
            except Exception:
                pass 
        
        membership_var.trace('w', update_expiry_date)
        joined_calendar.bind("<<DateEntrySelected>>", update_expiry_date)

        # Khung nút
        button_frame = ttk.Frame(edit_frame)
        button_frame.pack(pady=10)

        entries["save_btn"] = ttk.Button(button_frame, text="Save Changes", style="Success.TButton")
        entries["save_btn"].pack(side="left", padx=10)
        
        entries["delete_btn"] = ttk.Button(button_frame, text="Delete Member", style="Danger.TButton")
        entries["delete_btn"].pack(side="left", padx=10)
        
        # SỬA LỖI: Nút Cancel phải gọi hàm cancel_edit
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=cancel_edit, style="Warning.TButton")
        cancel_btn.pack(side="left", padx=10)
    
    # === Kết thúc tạo form ===

    def load_all_members():
        for item in tree.get_children(): tree.delete(item)
        all_members = admin.search_members("")
        for member in all_members:
            tree.insert("", "end", values=(
                member.get('username', 'N/A'), member.get('f_name', 'N/A'),
                member.get('l_name', 'N/A'), member.get('email', 'N/A'),
                member.get('phone', 'N/A'), member.get('membership', 'N/A'),
                member.get('subscription_expiry', 'N/A')
            ))
    
    def search_members():
        search_term = search_var.get().strip()
        for item in tree.get_children(): tree.delete(item)
        
        if not search_term:
            load_all_members()
            return
        
        found_members = admin.search_members(search_term)
        for member in found_members:
            tree.insert("", "end", values=(
                member.get('username', 'N/A'), member.get('f_name', 'N/A'),
                member.get('l_name', 'N/A'), member.get('email', 'N/A'),
                member.get('phone', 'N/A'), member.get('membership', 'N/A'),
                member.get('subscription_expiry', 'N/A')
            ))
        if not found_members:
            messagebox.showinfo("No Results", f"No members found matching '{search_term}'")

    def save_changes(member_username):
        values = {}
        for key, entry in entries.items():
            if key in ["save_btn", "delete_btn"]: continue
            
            if isinstance(entry, DateEntry):
                values[key] = entry.get_date().strftime('%Y-%m-%d')
            else:
                values[key] = entry.get()
        
        if any(v == "" for v in values.values()):
            messagebox.showerror("Error", "All fields must be filled!")
            return
        
        if admin.update_member(member_username, values):
            messagebox.showinfo("Success", "Member information updated successfully!")
            load_all_members()
            cancel_edit() # SỬA LỖI: Gọi hàm cancel_edit
        else:
            messagebox.showerror("Error", "Failed to update member information!")

    def delete_member(member_username, member_name):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete member '{member_name}' ({member_username})?"):
            if admin.delete_member(member_username):
                messagebox.showinfo("Success", "Member deleted successfully!")
                load_all_members()
                cancel_edit() # SỬA LỖI: Gọi hàm cancel_edit
            else:
                messagebox.showerror("Error", "Failed to delete member!")

    def show_edit_form(member):
        """TỐI ƯU: Chỉ cập nhật giá trị VÀ ẩn bảng results"""
        
        # SỬA LỖI: Ẩn bảng results để lấy không gian
        results_frame.pack_forget()

        # Cập nhật Entry
        for key in ["f_name", "l_name", "phone", "address", "email"]:
            entries[key].delete(0, 'end')
            entries[key].insert(0, member.get(key, ""))
            
        entries["gender"].set(member.get('gender', 'male'))
        
        try: dob_date = datetime.strptime(member.get('date_of_birth', '2000-01-01'), '%Y-%m-%d')
        except: dob_date = datetime(2000, 1, 1)
        entries["date_of_birth"].set_date(dob_date)
        
        try: joined_date = datetime.strptime(member.get('joined_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
        except: joined_date = datetime.now()
        entries["joined_date"].set_date(joined_date)
        
        try: expiry_date = datetime.strptime(member.get('subscription_expiry', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
        except: expiry_date = datetime.now()
        entries["subscription_expiry"].set_date(expiry_date)
        
        entries["membership"].set(member.get('membership', ''))
        entries["trainer_username"].set(member.get('trainer_username', ''))
        
        username = member.get('username')
        name = member.get('f_name', '')
        entries["save_btn"].config(command=lambda u=username: save_changes(u))
        entries["delete_btn"].config(command=lambda u=username, n=name: delete_member(u, n))

        # Hiển thị form
        edit_frame.pack(fill="both", expand=True, pady=10)

    def on_select_member(event):
        selection = tree.selection()
        if not selection: return
        
        selected_username = tree.item(selection[0])['values'][0]
        all_members = admin.search_members("")
        selected_member = next((m for m in all_members if m.get('username') == selected_username), None)
        
        if selected_member:
            show_edit_form(selected_member) 
            
    # === Bắt đầu chạy ===
    
    create_edit_form_structure() # Tạo cấu trúc form (đang ẩn)

    search_btn = ttk.Button(search_frame, text="Search", command=search_members, style="Primary.TButton")
    search_btn.pack(side="left", padx=10)
    
    show_all_btn = ttk.Button(search_frame, text="Show All Members", command=load_all_members, style="Success.TButton")
    show_all_btn.pack(side="left", padx=10)
    
    tree.bind("<<TreeviewSelect>>", on_select_member)
    
    back_btn = ttk.Button(main_frame, text="Back to Menu", command=root.destroy, style="Primary.TButton")
    back_btn.pack(side="bottom", pady=10)
    
    load_all_members()