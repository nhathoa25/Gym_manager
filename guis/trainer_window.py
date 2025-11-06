import tkinter as tk
from tkinter import messagebox
from utils.create_icon import c_icon #add the function to create the icon
from utils.create_background import c_background #add the function to create the background
from guis.trainer_guis.assigning_workout import on_assigning_workout
from guis.trainer_guis.add_attendance import on_add_attendance
import json
import os
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import ttk

# Placeholder functions for each feature
def on_assign_workout(root, trainer):
    on_assigning_workout(root, trainer)

def on_attendance_tracking(root, trainer):
    root.title("Attendance Tracking")
    tk.Label(root, text="Attendance Tracking (placeholder)", font=("Arial", 24)).pack(pady=50)

def on_adding_attendance(root, trainer):
    on_add_attendance(root, trainer)

def on_view_member_info(root, trainer):
    root.title("View Member Info")
    tk.Label(root, text="View Member Info (placeholder)", font=("Arial", 24)).pack(pady=50)

def on_progress_tracking(root, trainer):
    root.title("Progress Tracking")
    tk.Label(root, text="Progress Tracking (placeholder)", font=("Arial", 24)).pack(pady=50)

def on_top_member(root, trainer):
    root.title("Top Member")
    tk.Label(root, text="Top Member (placeholder)", font=("Arial", 24)).pack(pady=50)

def open_trainer_window(trainer):
    root = tk.Tk() #Create the main window
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    c_icon(root)
    c_background(root) #set the background of the window
    root.title("Gym Management System - Trainer") #set the title of the window

    # Track the current sub-window
    current_sub_window = None

    def close_sub_window():
        """Close the current sub-window if it exists"""
        nonlocal current_sub_window
        if current_sub_window and current_sub_window.winfo_exists():
            current_sub_window.destroy()
            current_sub_window = None

    def open_assign_workout():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_assign_workout(current_sub_window, trainer)

    def open_attendance_tracking():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_attendance_tracking(current_sub_window, trainer)

    def open_add_attendance():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_adding_attendance(current_sub_window, trainer)

    def open_view_member_info():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_view_member_info(current_sub_window, trainer)

    def open_progress_tracking():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_progress_tracking(current_sub_window, trainer)

    def open_top_member():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_top_member(current_sub_window, trainer)

    # Create buttons with the specified text
    btn_assign_workout = tk.Button(root, text="Assign Workout", command=open_assign_workout)
    btn_assign_workout.place(x=50, y=50, width=200, height=40)

    btn_attendance_tracking = tk.Button(root, text="Attendance Tracking", command=open_attendance_tracking)
    btn_attendance_tracking.place(x=300, y=50, width=200, height=40)

    btn_add_attendance = tk.Button(root, text="Add Attendance", command=open_add_attendance)
    btn_add_attendance.place(x=550, y=50, width=200, height=40)

    btn_view_member_info = tk.Button(root, text="View Member Info", command=open_view_member_info)
    btn_view_member_info.place(x=800, y=50, width=200, height=40)

    btn_progress_tracking = tk.Button(root, text="Progress Tracking", command=open_progress_tracking)
    btn_progress_tracking.place(x=1050, y=50, width=200, height=40)

    btn_top_member = tk.Button(root, text="Top Member", command=open_top_member)
    btn_top_member.place(x=1300, y=50, width=200, height=40)

    btn_exit = tk.Button(root, text="Exit", command=root.destroy)
    btn_exit.place(x=1550, y=50, width=150, height=40)
    
    root.mainloop()
