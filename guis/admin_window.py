import tkinter as tk
from tkinter import messagebox
from utils.create_icon import c_icon #add the function to create the icon
from utils.create_background import c_background #add the function to create the background
from guis.admin_guis.new_member import on_new_member
from guis.admin_guis.new_trainer import on_new_trainer
from guis.admin_guis.equipment_manager import on_equipment_manager
from guis.admin_guis.delete_member import on_delete_member
from guis.admin_guis.search_member import on_search_member
from guis.admin_guis.manage_subscription import on_manage_subscription
from guis.admin_guis.cal_revenue import on_cal_revenue
from guis.admin_guis.search_trainer import on_search_trainer
from guis.admin_guis.add_attendance import on_add_attendance

def open_admin_window(admin):
    root = tk.Tk() #Create the main window
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    c_icon(root)
    c_background(root) #set the background of the window
    root.title("Gym Management System - Admin") #set the title of the window

    # Track the current sub-window
    current_sub_window = None

    def close_sub_window():
        """Close the current sub-window if it exists"""
        nonlocal current_sub_window
        if current_sub_window and current_sub_window.winfo_exists():
            current_sub_window.destroy()
            current_sub_window = None

    def open_new_member():
        close_sub_window()  # Close any existing sub-window
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_new_member(current_sub_window, admin)
    
    def open_new_trainer():
        close_sub_window()  # Close any existing sub-window
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_new_trainer(current_sub_window, admin)
    
    def open_equipment_manager():
        close_sub_window()  # Close any existing sub-window
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_equipment_manager(current_sub_window, admin)
    
    def open_search_member():
        close_sub_window()  # Close any existing sub-window
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_search_member(current_sub_window, admin)

    def open_manage_subscription():
        close_sub_window()  # Close any existing sub-window
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_manage_subscription(current_sub_window, admin)

    def open_cal_revenue():
        close_sub_window()  # Close any existing sub-window
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_cal_revenue(current_sub_window, admin)

    def open_search_trainer():
        close_sub_window()  # Close any existing sub-window
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_search_trainer(current_sub_window, admin)

    def open_add_attendance():
        close_sub_window()  # Close any existing sub-window
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_add_attendance(current_sub_window, admin)

    # Create buttons with the specified text
    btn_new_member = tk.Button(root, text="New Member", command=open_new_member)
    btn_new_member.place(x=50, y=50, width=150, height=40)

    btn_new_trainer = tk.Button(root, text="New Trainer", command=open_new_trainer)
    btn_new_trainer.place(x=200, y=50, width=150, height=40)

    btn_equipment = tk.Button(root, text="Equipment", command=open_equipment_manager)
    btn_equipment.place(x=350, y=50, width=150, height=40)

    btn_search_member = tk.Button(root, text="Edit-Report Mem", command=open_search_member)
    btn_search_member.place(x=500, y=50, width=150, height=40)


    btn_subscription_plans = tk.Button(root, text="Subscription plans", command=open_manage_subscription)
    btn_subscription_plans.place(x=650, y=50, width=150, height=40)

    btn_cal_revenue = tk.Button(root, text="Revenue Report", command=open_cal_revenue)
    btn_cal_revenue.place(x=1100, y=50, width=150, height=40)

    btn_search_trainer = tk.Button(root, text="Edit Trainer", command=open_search_trainer)
    btn_search_trainer.place(x=800, y=50, width=150, height=40)

    btn_add_attendance = tk.Button(root, text="Add-Report Attendance", command=open_add_attendance)
    btn_add_attendance.place(x=950, y=50, width=150, height=40)

    btn_exit = tk.Button(root, text="Exit", command=root.destroy)
    btn_exit.place(x=1250, y=50, width=150, height=40)
    
    root.mainloop()
