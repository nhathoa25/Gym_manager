import tkinter as tk
import json
from utils.create_icon import c_icon
from utils.create_background import c_background


def show_member_workout_window(username, window=None):
    # Load member info
    with open("data/member_info.json", "r", encoding="utf-8") as f:
        members = json.load(f)
    member = next((m for m in members if m["username"] == username), None)

    root = window if window is not None else tk.Toplevel()
    root.title(f"Workout Days: {username}")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    c_icon(root)
    c_background(root)

    for widget in root.winfo_children():
        widget.destroy()

    if not member:
        tk.Label(root, text=f"No member found with username: {username}", font=("Arial", 16)).pack(pady=20)
        return

    tk.Label(root, text=f"Workout Days for {username}", font=("Arial", 20, "bold")).pack(pady=10)
    workout_days = member.get("workout_days", [])
    if not workout_days:
        tk.Label(root, text="No workout records found.", font=("Arial", 14)).pack(pady=10)
    else:
        frame = tk.Frame(root)
        frame.pack(pady=10)
        for day, workout in workout_days:
            day_str = f"Date: {day}"
            workout_str = f"Workout: {workout}"
            tk.Label(frame, text=day_str, font=("Arial", 13, "bold"), anchor="w", justify="left").pack(anchor="w", padx=10)
            tk.Label(frame, text=workout_str, font=("Arial", 12), anchor="w", justify="left").pack(anchor="w", padx=30, pady=(0, 8))
    btn = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12, "bold"))
    btn.pack(pady=20)
