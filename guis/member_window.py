import tkinter as tk
from utils.create_icon import c_icon
from utils.create_background import c_background
from guis.member_guis.check_info import show_member_info_window
from guis.member_guis.view_subscription import show_member_subscription_window
import os
import json
from guis.member_guis.contact import show_contact_window

# Placeholder functions for each feature
# def on_view_profile(root, member):
#     root.title("View Profile")
#     tk.Label(root, text="View Profile (placeholder)", font=("Arial", 24)).pack(pady=50)

def on_view_subscription(root, member):
    # Use the new function to show subscription info
    username = member.username if hasattr(member, 'username') else member['username']
    show_member_subscription_window(username)

def on_check_workout_schedule(root, member):
    username = member.username if hasattr(member, 'username') else member['username']
    from guis.member_guis.check_workout import show_member_workout_window
    show_member_workout_window(username, window=root)

def on_renew_subscribe_plan(root, member):
    root.title("Renew/Subscribe to New Plan")
    tk.Label(root, text="Renew or Subscribe to New Plan (placeholder)", font=("Arial", 24)).pack(pady=50)

def on_contact_trainers_admin(root, member):
    # Use member method to show contact info
    member.contact_trainers_admin()


def open_member_window(member):
    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    c_icon(root)
    c_background(root)
    root.title("Gym Management System - Member")

    current_sub_window = None

    def close_sub_window():
        nonlocal current_sub_window
        if current_sub_window and current_sub_window.winfo_exists():
            current_sub_window.destroy()
            current_sub_window = None

    def open_view_profile():
        # Use show_member_info_window directly
        username = member.username if hasattr(member, 'username') else member['username']
        show_member_info_window(username)

    def open_view_subscription():
        # Use the new function to show subscription info
        username = member.username if hasattr(member, 'username') else member['username']
        show_member_subscription_window(username)

    def open_check_workout_schedule():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_check_workout_schedule(current_sub_window, member)

    def open_renew_subscribe_plan():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_renew_subscribe_plan(current_sub_window, member)

    def open_contact_trainers_admin():
        # Always use the member's username to show the contact window
        username = member.username if hasattr(member, 'username') else member['username']
        show_contact_window(username)

    btn_view_profile = tk.Button(root, text="View Profile", command=open_view_profile)
    btn_view_profile.place(x=50, y=50, width=250, height=40)

    btn_view_subscription = tk.Button(root, text="View Subscription Plan", command=open_view_subscription)
    btn_view_subscription.place(x=350, y=50, width=250, height=40)

    btn_check_workout = tk.Button(root, text="Check Workout Schedule", command=open_check_workout_schedule)
    btn_check_workout.place(x=650, y=50, width=250, height=40)

    btn_renew_subscribe = tk.Button(root, text="Renew/Subscribe to New Plan", command=open_renew_subscribe_plan)
    btn_renew_subscribe.place(x=950, y=50, width=250, height=40)

    btn_contact = tk.Button(root, text="Contact Trainers / Admin", command=open_contact_trainers_admin)
    btn_contact.place(x=1250, y=50, width=250, height=40)

    btn_exit = tk.Button(root, text="Exit", command=root.destroy)
    btn_exit.place(x=1550, y=50, width=150, height=40)

    root.mainloop()
