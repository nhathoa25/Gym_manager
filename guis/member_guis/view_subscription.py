import tkinter as tk
import json
import os

def get_member_subscription_info(username):
    if not os.path.exists("data/member_info.json"):
        return None
    with open("data/member_info.json", "r", encoding="utf-8") as f:
        members = json.load(f)
    for m in members:
        if m.get("username") == username:
            return {
                'membership': m.get('membership'),
                'subscription_expiry': m.get('subscription_expiry'),
                'trainer_username': m.get('trainer_username'),
            }
    return None

def get_subscription_plan_detail(plan_name):
    if not os.path.exists("data/subscription_info.json"):
        return None
    with open("data/subscription_info.json", "r", encoding="utf-8") as f:
        plans = json.load(f)
    return plans.get(plan_name)

def show_member_subscription_window(username):
    info = get_member_subscription_info(username)
    root = tk.Toplevel()
    root.title("Your Subscription Plan")
    root.geometry("500x350")
    if not info:
        tk.Label(root, text=f"No subscription info found for: {username}", font=("Arial", 16)).pack(pady=20)
        root.mainloop()
        return
    plan_detail = get_subscription_plan_detail(info['membership'])
    tk.Label(root, text="Your Subscription Plan", font=("Arial", 20, "bold")).pack(pady=10)
    frame = tk.Frame(root)
    frame.pack(pady=10)
    tk.Label(frame, text=f"Plan: {info['membership']}", font=("Arial", 14)).pack(anchor="w")
    if plan_detail:
        if isinstance(plan_detail, list) and len(plan_detail) >= 2:
            tk.Label(frame, text=f"Duration: {plan_detail[0]} days", font=("Arial", 14)).pack(anchor="w")
            tk.Label(frame, text=f"Fee: {plan_detail[1]:,} VND", font=("Arial", 14)).pack(anchor="w")
    tk.Label(frame, text=f"Expiry Date: {info['subscription_expiry']}", font=("Arial", 14)).pack(anchor="w")
    tk.Label(frame, text=f"Trainer Username: {info['trainer_username']}", font=("Arial", 14)).pack(anchor="w")
    btn = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12, "bold"))
    btn.pack(pady=20)
