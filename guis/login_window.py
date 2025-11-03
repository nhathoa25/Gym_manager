import tkinter as tk
from tkinter import messagebox
from data_work.auth_add import check_credentials
from guis.register_window import open_register_window
from utils.create_icon import c_icon #add the function to create the icon
from guis.admin_window import open_admin_window
# from guis.trainer_window import open_trainer_window
# from guis.member_window import open_member_window

def open_login_window():
    result = {}
    root = tk.Tk() #Create the main window
    root.geometry("800x600")  # Set the size of the window to 800x600
    c_icon(root)
    root.title("Gym Management System - Login") #set the title of the window

    # ----------------------------------------------------
    # THÊM HIỆU ỨNG: TIÊU ĐỀ LỚN
    # ----------------------------------------------------
    
    # Định nghĩa phông chữ đậm và lớn
    TITLE_FONT = ("Arial", 20, "bold") 

    title_label = tk.Label(
        root, 
        text="WELLCOME TO THE GYM", 
        font=TITLE_FONT,
        fg="#0052cc"  # Màu chữ xanh dương
    )
    # Đặt tiêu đề ở vị trí cao hơn và căn giữa
    title_label.place(x=220, y=100) 

    # ----------------------------------------------------
    # Căn chỉnh các widget về giữa cửa sổ (điều chỉnh Y)
    # ----------------------------------------------------
    
    # Điều chỉnh Y_START thấp hơn (từ 250 xuống 250) để dành chỗ cho tiêu đề 
    label_x = 200 
    entry_x = 300
    y_start = 250 # Vị trí Y cho Username (Giữ nguyên hoặc điều chỉnh tùy ý)
    y_spacing = 40 # Khoảng cách giữa các dòng

    # Create labels and entry fields for username and password
    username_label = tk.Label(root, text="Username")
    password_label = tk.Label(root, text="Password")
    username_label.place(x=label_x, y=y_start)
    password_label.place(x=label_x, y=y_start + y_spacing)


    username_entry = tk.Entry(root, width=30)
    password_entry = tk.Entry(root, show="*", width=30)
    username_entry.place(x=entry_x, y=y_start)
    password_entry.place(x=entry_x, y=y_start + y_spacing)
    
    # Vị trí nút Login
    login_button_width = 10 
    login_button_x = 350 # Giữ nguyên vị trí X 

    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        role = check_credentials(username, password)
        if role != None:
            messagebox.showinfo("Login Successful", f"Logged in as {role.capitalize()}")
            root.destroy()  # Close login window
            result["username"] = username
            result["role"] = role
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            return

    login_button = tk.Button(root, text="Login", command=on_login, width=login_button_width)
    login_button.place(x=login_button_x, y=y_start + 2 * y_spacing) 
    
    # Vị trí link Register
    info_label = tk.Label(root, text="Don't have an account yet? ", bg=root["bg"])
    register_link = tk.Label(root, text="Register", fg="blue", cursor="hand2", bg=root["bg"], underline=True)
    
    info_label.place(x=300, y=y_start + 3 * y_spacing) 
    register_link.place(x=450, y=y_start + 3 * y_spacing)


    def on_register():
        root.destroy() # Close login window
        open_register_window() # Open the register window

    def on_click(evene = None):
        on_register()
        
    register_link.bind("<Button-1>", on_click)
 
    root.mainloop()
    return result.get("username"), result.get("role")