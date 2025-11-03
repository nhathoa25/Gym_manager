import tkinter as tk
import json

ADMIN_PHONE = "0977889999"

def get_trainer_phone(trainer_username):
    """Return the phone number of the trainer with the given username, or None if not found."""
    with open("data/trainer_info.json", "r", encoding="utf-8") as f:
        trainers = json.load(f)
    for trainer in trainers:
        if trainer.get("username") == trainer_username:
            return trainer.get("phone")
    return None

def show_contact_window(member_username):
    """Show a window with the trainer's phone and the admin phone for the given member."""
    # Get the trainer username for this member
    with open("data/member_info.json", "r", encoding="utf-8") as f:
        members = json.load(f)
    trainer_username = None
    for member in members:
        if member.get("username") == member_username:
            trainer_username = member.get("trainer_username")
            break
    trainer_phone = get_trainer_phone(trainer_username) if trainer_username else None

    win = tk.Toplevel()
    win.title("Contact Trainer / Admin")
    win.geometry("400x200")

    tk.Label(win, text=f"Trainer's Phone:", font=("Arial", 14)).pack(pady=(20, 0))
    if trainer_phone:
        tk.Label(win, text=trainer_phone, font=("Arial", 16, "bold"), fg="blue").pack()
    else:
        tk.Label(win, text="Not assigned", font=("Arial", 16, "bold"), fg="red").pack()

    tk.Label(win, text=f"Admin's Phone:", font=("Arial", 14)).pack(pady=(20, 0))
    tk.Label(win, text=ADMIN_PHONE, font=("Arial", 16, "bold"), fg="green").pack()

    tk.Button(win, text="Close", command=win.destroy).pack(pady=20)
