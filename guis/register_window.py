import tkinter as tk
from tkinter import messagebox
from data_work.auth_add import check_credentials
from data_work.auth_add import add_user_to_json
from utils.create_icon import c_icon #add the function to create the icon


def open_register_window():
    root = tk.Tk() #Create the main window
    #root.geometry("300x200")  # Set the size of the window
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    c_icon(root)
    root.title("Gym Management System - Register") #set the title of the window

    # Create labels and entry fields for username and password
    
    username_label = tk.Label(root, text="Username")
    password_label = tk.Label(root, text="Password")
    repassword_label = tk.Label(root, text="Comfirm password")
    username_label.place(x=30, y=30)
    password_label.place(x=30, y=70)
    repassword_label.place(x=30, y=110)


    username_entry = tk.Entry(root)
    password_entry = tk.Entry(root, show="*")
    repassword_entry = tk.Entry(root, show="*")
    username_entry.place(x=100, y=30)
    password_entry.place(x=100, y=70)
    repassword_entry.place(x=100, y=110)

    # Replace Text widget with Label widgets
    info_label = tk.Label(root, text="Already have an account? ", bg=root["bg"])
    info_label.place(x=20, y=150)

    login_link = tk.Label(root, text="Login", fg="blue", cursor="hand2", bg=root["bg"], underline=True)
    login_link.place(x=162, y=150)

    def on_click(event=None):
        root.destroy()
        from guis.login_window import open_login_window
        open_login_window()

    login_link.bind("<Button-1>", on_click)

    def on_register():
        username = username_entry.get()
        password = password_entry.get()
        repassword = repassword_entry.get()
        if password != repassword:
            messagebox.showerror("Registration Failed", "Passwords do not match")
            return
        else:
            if check_credentials(username, password) != None:
                messagebox.showerror("Registration Failed", "Username already exists")
                return
            if username == "" or password == "" or repassword == "":
                messagebox.showerror("Registration Failed", "Username and password cannot be empty")
                return
            add_user_to_json(username, password, "member")
            messagebox.showinfo("Registration Successful", "You can now login with your credentials")
            root.destroy()
            from guis.login_window import open_login_window  # Move import here
            open_login_window()  # Open the login window after registration
       

    register_button = tk.Button(root, text="Register", command=on_register)
    register_button.place(x=200, y=120)


    root.mainloop()
