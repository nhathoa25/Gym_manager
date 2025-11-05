import tkinter as tk
from tkinter import messagebox
from data_work.auth_add import check_credentials
from guis.register_window import open_register_window
from utils.create_icon import c_icon

def open_login_window():
    result = {}
    root = tk.Tk()
    root.geometry("800x600")
    c_icon(root)
    root.title("Gym Management System - Login")
    root.configure(bg="#f0f2f5")  

    # Fonts
    TITLE_FONT = ("Segoe UI", 28, "bold") 
    LABEL_FONT = ("Segoe UI", 12)
    ENTRY_FONT = ("Segoe UI", 12)
    BUTTON_FONT = ("Segoe UI", 13, "bold")
    CHECK_FONT = ("Segoe UI", 10) # Font cho Checkbutton

    # Tiêu đề
    title_label = tk.Label(
        root,
        text="WELCOME TO THE GYM",
        font=TITLE_FONT,
        fg="#1877f2", 
        bg=root["bg"]
    )
    title_label.place(relx=0.5, y=100, anchor="center")

    # Form Frame
    form_frame = tk.Frame(root, bg="#ffffff", padx=30, pady=20, 
                          highlightbackground="#ccc", highlightthickness=1, 
                          relief="flat")
    form_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=330) # Tăng nhẹ chiều cao form

    # --- INPUT FIELDS (Sử dụng GRID) ---

    def create_underline_entry(parent, show_char=""):
        entry = tk.Entry(parent, font=ENTRY_FONT, width=35, 
                         relief="flat", bg="#ffffff", bd=0, 
                         highlightthickness=1, highlightbackground="#ccc", highlightcolor="#1877f2")
        if show_char:
            entry.config(show=show_char)
        return entry
    
    # Username
    username_label = tk.Label(form_frame, text="Username:", font=LABEL_FONT, bg="white", anchor="w")
    username_label.grid(row=0, column=0, sticky="w", pady=(15, 5), padx=5)

    username_entry = create_underline_entry(form_frame)
    username_entry.grid(row=1, column=0, sticky="ew", pady=(0, 15), padx=5)

    # Password
    password_label = tk.Label(form_frame, text="Password:", font=LABEL_FONT, bg="white", anchor="w")
    password_label.grid(row=2, column=0, sticky="w", pady=(5, 5), padx=5)

    password_entry = create_underline_entry(form_frame, show_char="*")
    password_entry.grid(row=3, column=0, sticky="ew", pady=(0, 5), padx=5)
    
    # --- SHOW PASSWORD CHECKBOX ---
    
    show_password_var = tk.StringVar(value="0") # Biến lưu trạng thái checkbox (0: Ẩn, 1: Hiện)
    
    def toggle_password_visibility():
        if show_password_var.get() == "1":
            # Nếu được check, hiện mật khẩu (show='')
            password_entry.config(show="")
        else:
            # Nếu không được check, ẩn mật khẩu (show='*')
            password_entry.config(show="*")
            
    show_password_check = tk.Checkbutton(
        form_frame,
        text="Show Password",
        font=CHECK_FONT,
        bg="white",
        fg="#444",
        variable=show_password_var,
        onvalue="1",
        offvalue="0",
        command=toggle_password_visibility,
        relief="flat"
    )
    # Đặt Checkbutton ngay dưới ô nhập mật khẩu, căn phải
    show_password_check.grid(row=4, column=0, sticky="e", pady=(5, 10), padx=5)


    form_frame.grid_columnconfigure(0, weight=1) 

    # --- BUTTON LOGIN ---

    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        role = check_credentials(username, password) 
        if role:
            messagebox.showinfo("Login Successful", f"Logged in as {role.capitalize()}")
            root.destroy()
            result["username"] = username
            result["role"] = role
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_button = tk.Button(
        form_frame,
        text="Login",
        font=BUTTON_FONT,
        width=25, 
        height=1,
        bg="#1877f2", 
        fg="white",
        activebackground="#0e62c2",
        cursor="hand2",
        command=on_login,
        relief="flat", 
        bd=0
    )
    # Thay đổi row từ 4 sang 5 (vì đã thêm Checkbutton vào row 4)
    login_button.grid(row=5, column=0, pady=(15, 0), padx=5, sticky="n")

    # Thêm hiệu ứng hover (giữ nguyên)
    def on_enter(e):
        login_button.config(bg="#0e62c2")
    def on_leave(e):
        login_button.config(bg="#1877f2")
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    # --- REGISTER LINK ---
    info_label = tk.Label(root, text="Don't have an account?", font=("Segoe UI", 11), bg=root["bg"]) 
    info_label.place(relx=0.5, y=520, anchor="e", x=-20) # Điều chỉnh vị trí y xuống 520

    register_link = tk.Label(root, text="Register", font=("Segoe UI", 11, "underline"), fg="#1877f2", cursor="hand2", bg=root["bg"]) 
    register_link.place(relx=0.5, y=520, anchor="w", x=20) # Điều chỉnh vị trí y xuống 520

    def on_register(event=None):
        root.destroy()
        open_register_window()

    register_link.bind("<Button-1>", on_register)

    root.mainloop()
    return result.get("username"), result.get("role")