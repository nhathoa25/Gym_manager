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

    # Tiêu đề
    title_label = tk.Label(
        root,
        text="WELCOME TO THE GYM",
        font=TITLE_FONT,
        fg="#1877f2", 
        bg=root["bg"]
    )
    title_label.place(relx=0.5, y=100, anchor="center")

    # Form Frame - Viền mỏng bên ngoài vẫn giữ
    form_frame = tk.Frame(root, bg="#ffffff", padx=30, pady=20, 
                          highlightbackground="#ccc", highlightthickness=1, 
                          relief="flat")
    form_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=300) # Điều chỉnh rely nhẹ để có không gian cho link bên dưới

    # --- INPUT FIELDS (Sử dụng GRID) ---

    # Hàm tạo Entry field kiểu Underline (Đường viền dưới)
    def create_underline_entry(parent, show_char=""):
        # Tạo Entry field PHẲNG hoàn toàn
        entry = tk.Entry(parent, font=ENTRY_FONT, width=35, 
                         relief="flat", bg="#ffffff", bd=0, 
                         highlightthickness=1, highlightbackground="#ccc", highlightcolor="#1877f2")
        # Sử dụng thuộc tính highlight để tạo đường viền dưới mượt mà hơn
        if show_char:
            entry.config(show=show_char)
        return entry
    
    # Username
    username_label = tk.Label(form_frame, text="Username:", font=LABEL_FONT, bg="white", anchor="w")
    username_label.grid(row=0, column=0, sticky="w", pady=(15, 5), padx=5)

    username_entry = create_underline_entry(form_frame)
    username_entry.grid(row=1, column=0, sticky="ew", pady=(0, 20), padx=5)

    # Password
    password_label = tk.Label(form_frame, text="Password:", font=LABEL_FONT, bg="white", anchor="w")
    password_label.grid(row=2, column=0, sticky="w", pady=(5, 5), padx=5)

    password_entry = create_underline_entry(form_frame, show_char="*")
    password_entry.grid(row=3, column=0, sticky="ew", pady=(0, 25), padx=5)
    
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
    login_button.grid(row=4, column=0, pady=(15, 0), padx=5, sticky="n")

    # Thêm hiệu ứng hover
    def on_enter(e):
        login_button.config(bg="#0e62c2")
    def on_leave(e):
        login_button.config(bg="#1877f2")
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    # --- REGISTER LINK ---
    # Điều chỉnh vị trí y để link nằm dưới khung form, không bị lấn vào
    link_y_pos = form_frame.winfo_y() + 300 + 30 # y của form + height của form + padding
    
    info_label = tk.Label(root, text="Don't have an account?", font=("Segoe UI", 11), bg=root["bg"]) 
    info_label.place(relx=0.5, y=490, anchor="e", x=-20) 

    register_link = tk.Label(root, text="Register", font=("Segoe UI", 11, "underline"), fg="#1877f2", cursor="hand2", bg=root["bg"]) 
    register_link.place(relx=0.5, y=490, anchor="w", x=20) 

    def on_register(event=None):
        root.destroy()
        open_register_window()

    register_link.bind("<Button-1>", on_register)

    root.mainloop()
    return result.get("username"), result.get("role")