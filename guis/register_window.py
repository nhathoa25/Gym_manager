import tkinter as tk
from tkinter import messagebox
from data_work.auth_add import check_credentials, add_user_to_json
from utils.create_icon import c_icon

def open_register_window():
    root = tk.Tk()
    root.geometry("800x600")
    c_icon(root)
    root.title("Gym Management System - Register")
    root.configure(bg="#f0f2f5")

    # Fonts
    TITLE_FONT = ("Segoe UI", 28, "bold")
    LABEL_FONT = ("Segoe UI", 12)
    ENTRY_FONT = ("Segoe UI", 12)
    BUTTON_FONT = ("Segoe UI", 13, "bold")

    # Title
    title_label = tk.Label(
        root,
        text="CREATE NEW ACCOUNT", # Dịch: TẠO TÀI KHOẢN MỚI
        font=TITLE_FONT,
        fg="#1877f2", 
        bg=root["bg"]
    )
    title_label.place(relx=0.5, y=100, anchor="center")

    # Form Frame
    form_frame = tk.Frame(root, bg="#ffffff", padx=30, pady=20, highlightbackground="#ccc", highlightthickness=1, relief="flat") 
    form_frame.place(relx=0.5, rely=0.55, anchor="center", width=450, height=350)
    
    # Hàng 1: Username
    tk.Label(form_frame, text="Username:", font=LABEL_FONT, bg="white", anchor="w").grid(row=0, column=0, sticky="w", pady=(15, 5), padx=5) # Dịch: Tên đăng nhập
    username_entry = tk.Entry(form_frame, font=ENTRY_FONT, width=35, relief="flat", bg="#f7f7f7", bd=0) 
    username_entry.grid(row=1, column=0, sticky="ew", pady=(0, 15), padx=5, columnspan=2)

    # Hàng 2: Password
    tk.Label(form_frame, text="Password:", font=LABEL_FONT, bg="white", anchor="w").grid(row=2, column=0, sticky="w", pady=(5, 5), padx=5) # Dịch: Mật khẩu
    password_entry = tk.Entry(form_frame, font=ENTRY_FONT, width=35, show="*", relief="flat", bg="#f7f7f7", bd=0)
    password_entry.grid(row=3, column=0, sticky="ew", pady=(0, 15), padx=5, columnspan=2)

    # Hàng 3: Confirm Password
    tk.Label(form_frame, text="Confirm Password:", font=LABEL_FONT, bg="white", anchor="w").grid(row=4, column=0, sticky="w", pady=(5, 5), padx=5) # Dịch: Xác nhận Mật khẩu
    repassword_entry = tk.Entry(form_frame, font=ENTRY_FONT, width=35, show="*", relief="flat", bg="#f7f7f7", bd=0)
    repassword_entry.grid(row=5, column=0, sticky="ew", pady=(0, 25), padx=5, columnspan=2)
    
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=1)

    # Register logic
    def on_register():
        username = username_entry.get()
        password = password_entry.get()
        repassword = repassword_entry.get()

        # Dịch: Vui lòng điền đầy đủ tất cả các trường.
        if not username or not password or not repassword:
            messagebox.showerror("Error", "All fields are required.")
            return
        # Dịch: Mật khẩu xác nhận không khớp.
        if password != repassword:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        
        try:
            # Dịch: Tên đăng nhập đã tồn tại.
            if check_credentials(username, password) is not None:
                 messagebox.showerror("Error", "Username already exists.")
                 return
        except Exception:
            pass
            
        try:
            add_user_to_json(username, password, "member")
            # Dịch: Tài khoản đã được tạo thành công!
            messagebox.showinfo("Success", "Account created successfully!")
            root.destroy()
            from guis.login_window import open_login_window
            open_login_window()
        # Dịch: Không thể tạo tài khoản. Lỗi: {e}
        except Exception as e:
            messagebox.showerror("Error", f"Could not create account. Error: {e}")


    # Button with hover
    register_button = tk.Button(
        form_frame,
        text="Register", # Dịch: Đăng Ký
        font=BUTTON_FONT,
        bg="#1877f2", 
        fg="white",
        activebackground="#0e62c2", 
        cursor="hand2",
        width=25,
        height=1,
        command=on_register,
        relief="flat", 
        bd=0
    )
    register_button.grid(row=6, column=0, columnspan=2, pady=(15, 0), padx=5, sticky="n") 
    
    def on_enter(e):
        register_button.config(bg="#0e62c2")
    def on_leave(e):
        register_button.config(bg="#1877f2")
    register_button.bind("<Enter>", on_enter)
    register_button.bind("<Leave>", on_leave)

    # Login link
    info_label = tk.Label(root, text="Already have an account?", font=("Segoe UI", 11), bg=root["bg"]) # Dịch: Bạn đã có tài khoản?
    info_label.place(relx=0.5, y=550, anchor="e", x=-20) 
    
    login_link = tk.Label(root, text="Login", font=("Segoe UI", 11, "underline"), fg="#1877f2", cursor="hand2", bg=root["bg"]) # Dịch: Đăng nhập
    login_link.place(relx=0.5, y=550, anchor="w", x=20)

    def go_to_login(event=None):
        root.destroy()
        from guis.login_window import open_login_window
        open_login_window()

    login_link.bind("<Button-1>", go_to_login)

    root.mainloop()