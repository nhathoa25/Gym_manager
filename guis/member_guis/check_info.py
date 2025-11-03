import tkinter as tk
from models.member import Member
import json
import os



def show_member_info_window(username):
    member = Member.get_member_info(username)
    root = tk.Toplevel()
    root.title(f"Member Info: {username}")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    if not member:
        tk.Label(root, text=f"No member found with username: {username}", font=("Arial", 16)).pack(pady=20)
        root.mainloop()
        return
    tk.Label(root, text=f"Member Profile: {username}", font=("Arial", 20, "bold")).pack(pady=10)
    info_frame = tk.Frame(root)
    info_frame.pack(pady=10)
    for key, value in member.items():
        tk.Label(info_frame, text=f"{key}: {value}", font=("Arial", 12), anchor="w", justify="left").pack(anchor="w")
    btn = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12, "bold"))
    btn.pack(pady=20)
    root.mainloop()
