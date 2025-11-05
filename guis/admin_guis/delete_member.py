import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

def load_members_data():
    filepath = "data/member_info.json"
    if not os.path.exists(filepath): return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def on_delete_member(root, admin):
    text_label = ttk.Label(root, text="Delete Member", font=("Arial", 24))
    text_label.pack(pady=20)

    main_frame = ttk.Frame(root)
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Khung danh sách
    list_frame = ttk.Frame(main_frame)
    list_frame.pack(fill="both", expand=True, pady=10)
    
    list_title = ttk.Label(list_frame, text="Current Members:", font=("Arial", 14, "bold"))
    list_title.pack(anchor="w", pady=(0, 10))
    
    # Sử dụng Treeview thay vì Text
    columns = ("Username", "Name", "Email")
    tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
    tree.heading("Username", text="Username")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.column("Username", width=150)
    tree.column("Name", width=200)
    tree.column("Email", width=250)

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def refresh_member_list():
        # Xóa
        for item in tree.get_children():
            tree.delete(item)
        # Tải lại
        members = load_members_data()
        for member in members:
            name = f"{member.get('f_name', 'N/A')} {member.get('l_name', 'N/A')}"
            tree.insert("", "end", values=(
                member.get('username', 'N/A'),
                name,
                member.get('email', 'N/A')
            ))
        return members # Trả về danh sách đã tải

    members = refresh_member_list()
    
    # Input frame
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(pady=20)
    
    username_label = ttk.Label(input_frame, text="Enter Username to Delete:", font=("Arial", 12))
    username_label.pack(side="left", padx=(0, 10))
    
    username_var = tk.StringVar()
    username_entry = ttk.Entry(input_frame, textvariable=username_var, font=("Arial", 12), width=30)
    username_entry.pack(side="left")
    
    # Tự động điền khi chọn
    def on_member_select(event):
        selection = tree.selection()
        if selection:
            username = tree.item(selection[0])['values'][0]
            username_var.set(username)
            
    tree.bind("<<TreeviewSelect>>", on_member_select)
    
    def delete_member():
        username = username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter or select a username!")
            return
        
        # Tải lại danh sách mới nhất để kiểm tra
        current_members = load_members_data()
        if not any(member.get('username') == username for member in current_members):
            messagebox.showerror("Error", f"Member with username '{username}' not found!")
            return
        
        if messagebox.askyesno("Confirm Deletion", 
                                   f"Are you sure you want to delete member '{username}'?\nThis action cannot be undone."):
            if admin.delete_member(username):
                messagebox.showinfo("Success", f"Member '{username}' has been deleted successfully!")
                username_var.set("")
                refresh_member_list() # Tải lại danh sách
            else:
                messagebox.showerror("Error", f"Failed to delete member '{username}'!")
    
    # Khung nút
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(side="bottom", pady=20)

    delete_btn = ttk.Button(button_frame, text="Delete Member", command=delete_member, style="Danger.TButton")
    delete_btn.pack(side="left", padx=10)

    back_btn = ttk.Button(button_frame, text="Back to Menu", command=root.destroy, style="Primary.TButton")
    back_btn.pack(side="left", padx=10)