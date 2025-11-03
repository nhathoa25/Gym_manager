import tkinter as tk
from tkinter import messagebox
import json
import os

def load_members_data():
    """Load current members data to display in the list"""
    filepath = "data/member_info.json"
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def on_delete_member(root, admin):
    root.title("Delete Member")
    text_label = tk.Label(root, text="Delete Member", font=("Arial", 24), bg=root["bg"])
    text_label.pack(pady=20)

    main_frame = tk.Frame(root, bg=root["bg"])
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Load current members
    members = load_members_data()
    
    # Create a frame for the list
    list_frame = tk.Frame(main_frame, bg=root["bg"])
    list_frame.pack(fill="both", expand=True, pady=10)
    
    # Title for the list
    list_title = tk.Label(list_frame, text="Current Members:", font=("Arial", 14, "bold"), bg=root["bg"])
    list_title.pack(anchor="w", pady=(0, 10))
    
    # Create a text widget to display members
    members_text = tk.Text(list_frame, height=10, width=50, font=("Arial", 10))
    members_text.pack(fill="both", expand=True)
    
    # Populate the text widget with member information
    for member in members:
        member_info = f"Username: {member.get('username', 'N/A')} | Name: {member.get('f_name', 'N/A')} {member.get('l_name', 'N/A')} | Email: {member.get('email', 'N/A')}\n"
        members_text.insert(tk.END, member_info)
    
    members_text.config(state="disabled")  # Make it read-only
    
    # Input frame
    input_frame = tk.Frame(main_frame, bg=root["bg"])
    input_frame.pack(pady=20)
    
    # Username input
    username_label = tk.Label(input_frame, text="Enter Username to Delete:", font=("Arial", 12), bg=root["bg"])
    username_label.pack(anchor="w")
    
    username_var = tk.StringVar()
    username_entry = tk.Entry(input_frame, textvariable=username_var, font=("Arial", 12), width=30)
    username_entry.pack(pady=5)
    
    def delete_member():
        username = username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            return
        
        # Check if member exists
        member_exists = any(member.get('username') == username for member in members)
        if not member_exists:
            messagebox.showerror("Error", f"Member with username '{username}' not found!")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("Confirm Deletion", 
                                   f"Are you sure you want to delete member '{username}'?\n\nThis action cannot be undone.")
        if result:
            if admin.delete_member(username):
                messagebox.showinfo("Success", f"Member '{username}' has been deleted successfully!")
                username_var.set("")  # Clear the input
                # Refresh the member list
                members_text.config(state="normal")
                members_text.delete(1.0, tk.END)
                updated_members = load_members_data()
                for member in updated_members:
                    member_info = f"Username: {member.get('username', 'N/A')} | Name: {member.get('f_name', 'N/A')} {member.get('l_name', 'N/A')} | Email: {member.get('email', 'N/A')}\n"
                    members_text.insert(tk.END, member_info)
                members_text.config(state="disabled")
            else:
                messagebox.showerror("Error", f"Failed to delete member '{username}'!")
    
    # Button frame for Delete and Back buttons
    button_frame = tk.Frame(main_frame, bg=root["bg"])
    button_frame.pack(pady=20)

    delete_btn = tk.Button(button_frame, text="Delete Member", command=delete_member, 
                          font=("Arial", 14, "bold"), bg="#f44336", fg="white", 
                          relief="raised", bd=2)
    delete_btn.pack(side="left", padx=10)

    def back_to_menu():
        root.destroy()

    back_btn = tk.Button(button_frame, text="Back to Menu", command=back_to_menu,
                        font=("Arial", 14, "bold"), bg="#2196F3", fg="white",
                        relief="raised", bd=2)
    back_btn.pack(side="left", padx=10)
