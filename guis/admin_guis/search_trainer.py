import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import json
import os

def load_all_trainers():
    if not os.path.exists("data/trainer_info.json"):
        return []
    try:
        with open("data/trainer_info.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_all_trainers(trainers):
    try:
        with open("data/trainer_info.json", "w", encoding="utf-8") as f:
            json.dump(trainers, f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False

def on_search_trainer(root, admin):
    root.title("Search and Edit Trainer")
    text_label = ttk.Label(root, text="Search and Edit Trainer", font=("Arial", 24))
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

    # Results frame (Sẽ được ẩn/hiện)
    results_frame = ttk.Frame(main_frame)
    results_frame.pack(fill="both", expand=True, pady=10) # Hiển thị ban đầu

    columns = ("Username", "First Name", "Last Name", "Email", "Phone", "Trainer ID", "Height", "Weight")
    tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=8)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110)
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # === TỐI ƯU HÓA: Tạo form chỉnh sửa 1 LẦN (ban đầu ẩn) ===
    edit_frame = ttk.Frame(main_frame) 
    entries = {} 

    def cancel_edit():
        """Ẩn form edit và hiện lại bảng results"""
        edit_frame.pack_forget()
        results_frame.pack(fill="both", expand=True, pady=10)

    def create_edit_form_structure():
        """Tạo cấu trúc form 1 lần, lưu widget vào 'entries'"""
        
        form_grid = ttk.Frame(edit_frame)
        form_grid.pack(fill="x", expand=True, pady=10)
        form_grid.columnconfigure(1, weight=1) 
        
        fields = [
            ("First Name", "f_name"), ("Last Name", "l_name"),
            ("Phone", "phone"), ("Address", "address"),
            ("Email", "email"), ("Username", "username"),
            ("Height (cm)", "height"), ("Weight (kg)", "weight"),
            ("Trainer ID", "trainer_id"),
            ("Member Usernames (cách nhau bởi dấu phẩy)", "member_username")
        ]
        
        row_index = 0
        for label_text, key in fields:
            label = ttk.Label(form_grid, text=label_text, font=("Arial", 11))
            label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
            
            entry = ttk.Entry(form_grid, font=("Arial", 11))
            # TỐI ƯU CĂN CHỈNH: sticky="ew" làm widget co giãn bằng nhau
            entry.grid(row=row_index, column=1, sticky="ew", padx=10, pady=5)
            entries[key] = entry
            row_index += 1

        # Gender
        label = ttk.Label(form_grid, text="Gender", font=("Arial", 11))
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
        gender_var = tk.StringVar()
        gender_frame = ttk.Frame(form_grid)
        gender_frame.grid(row=row_index, column=1, sticky="w", padx=10, pady=5) 
        male_radio = ttk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="male")
        male_radio.pack(side="left", padx=(0, 20))
        female_radio = ttk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="female")
        female_radio.pack(side="left")
        entries["gender"] = gender_var
        row_index += 1

        # DOB
        label = ttk.Label(form_grid, text="Date of Birth", font=("Arial", 11))
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
        dob_cal = DateEntry(form_grid, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        dob_cal.grid(row=row_index, column=1, sticky="ew", padx=10, pady=5) 
        entries["date_of_birth"] = dob_cal
        row_index += 1
        
        # Joined Date
        label = ttk.Label(form_grid, text="Joined Date", font=("Arial", 11))
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
        joined_cal = DateEntry(form_grid, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        joined_cal.grid(row=row_index, column=1, sticky="ew", padx=10, pady=5) 
        entries["joined_date"] = joined_cal
        row_index += 1

        # Khung nút
        button_frame = ttk.Frame(edit_frame)
        button_frame.pack(pady=20) # Đặt ở cuối edit_frame
        
        entries["save_btn"] = ttk.Button(button_frame, text="Save Changes", style="Success.TButton")
        entries["save_btn"].pack(side="left", padx=10)
        
        entries["delete_btn"] = ttk.Button(button_frame, text="Delete Trainer", style="Danger.TButton")
        entries["delete_btn"].pack(side="left", padx=10)
        
        # SỬA LỖI: Nút Cancel phải gọi hàm cancel_edit
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=cancel_edit, style="Warning.TButton")
        cancel_btn.pack(side="left", padx=10)

    # === Kết thúc tạo form ===

    def refresh_trainer_list(trainers):
        for item in tree.get_children(): tree.delete(item)
        for trainer in trainers:
            tree.insert("", "end", values=(
                trainer.get('username', ''), trainer.get('f_name', ''),
                trainer.get('l_name', ''), trainer.get('email', ''),
                trainer.get('phone', ''), trainer.get('trainer_id', ''),
                trainer.get('height', ''), trainer.get('weight', '')
            ))

    def search_trainers():
        search_term = search_var.get().strip()
        found = admin.search_trainer(search_term) 
        refresh_trainer_list(found)
        if not found:
            messagebox.showinfo("No Results", f"No trainers found matching '{search_term}'")

    def save_changes(trainer_to_update):
        all_trainers = load_all_trainers()
        for t in all_trainers:
            if t.get('username') == trainer_to_update.get('username'):
                for key, widget in entries.items():
                    if key in ["save_btn", "delete_btn"]: continue
                    
                    if isinstance(widget, DateEntry):
                        t[key] = widget.get_date().strftime('%Y-%m-%d')
                    elif key == "gender":
                        t[key] = widget.get()
                    elif key == "member_username":
                        t[key] = [u.strip() for u in widget.get().split(',') if u.strip()]
                    elif hasattr(widget, 'get'):
                        t[key] = widget.get()
                break
                
        if save_all_trainers(all_trainers):
            messagebox.showinfo("Success", "Trainer information updated successfully!")
            refresh_trainer_list(all_trainers)
            cancel_edit() # SỬA LỖI: Ẩn form edit sau khi lưu
        else:
            messagebox.showerror("Error", "Failed to save trainer data!")

    def delete_trainer(trainer_to_delete):
        username = trainer_to_delete.get('username')
        name = trainer_to_delete.get('f_name', '')
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete trainer '{name}' ({username})?"):
            all_trainers = load_all_trainers()
            all_trainers = [t for t in all_trainers if t.get('username') != username]
            
            if save_all_trainers(all_trainers):
                messagebox.showinfo("Success", "Trainer deleted successfully!")
                refresh_trainer_list(all_trainers)
                cancel_edit() # SỬA LỖI: Ẩn form edit sau khi xóa
            else:
                messagebox.showerror("Error", "Failed to save trainer data!")

    def show_edit_form(trainer):
        """TỐI ƯU: Chỉ cập nhật giá trị, không tạo lại widget"""
        
        # SỬA LỖI: Ẩn bảng kết quả
        results_frame.pack_forget()

        # Cập nhật Entry
        fields = ["f_name", "l_name", "phone", "address", "email", "username", "height", "weight", "trainer_id"]
        for key in fields:
            entries[key].delete(0, 'end')
            entries[key].insert(0, str(trainer.get(key, "")))
            
        members = trainer.get('member_username', [])
        entries["member_username"].delete(0, 'end')
        entries["member_username"].insert(0, ', '.join(members))
            
        # Cập nhật Radio
        entries["gender"].set(trainer.get('gender', 'male'))
        
        # Cập nhật Lịch
        try: dob_date = datetime.strptime(trainer.get('date_of_birth', '2000-01-01'), '%Y-%m-%d')
        except: dob_date = datetime(2000, 1, 1)
        entries["date_of_birth"].set_date(dob_date)
        
        try: joined_date = datetime.strptime(trainer.get('joined_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
        except: joined_date = datetime.now()
        entries["joined_date"].set_date(joined_date)
        
        # Cập nhật lệnh cho nút
        entries["save_btn"].config(command=lambda t=trainer: save_changes(t))
        entries["delete_btn"].config(command=lambda t=trainer: delete_trainer(t))

        # Hiển thị form
        edit_frame.pack(fill="both", expand=True, pady=10)

    def on_select_trainer(event):
        selection = tree.selection()
        if not selection: return
        selected_username = tree.item(selection[0])['values'][0]
        all_trainers = load_all_trainers()
        selected_trainer = next((t for t in all_trainers if t.get('username') == selected_username), None)
        if selected_trainer:
            show_edit_form(selected_trainer)

    # === Bắt đầu chạy ===
    
    # Tạo cấu trúc form (đang ẩn)
    create_edit_form_structure()
    
    tree.bind("<<TreeviewSelect>>", on_select_trainer)
    
    def show_all():
        refresh_trainer_list(admin.search_trainer(""))
        
    search_btn = ttk.Button(search_frame, text="Search", command=search_trainers, style="Primary.TButton")
    search_btn.pack(side="left", padx=10)
    
    show_all_btn = ttk.Button(search_frame, text="Show All Trainers", command=show_all, style="Success.TButton")
    show_all_btn.pack(side="left", padx=10)
    
    show_all() # Tải danh sách ban đầu
    
    back_btn = ttk.Button(main_frame, text="Back to Menu", command=root.destroy, style="Primary.TButton")
    back_btn.pack(side="bottom", pady=10)