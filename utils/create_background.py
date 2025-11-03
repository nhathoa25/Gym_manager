import tkinter as tk
from PIL import Image, ImageTk

def c_background(window: tk.Tk):

    # Load and resize the background image
    bg_image = Image.open("assets/background_v2.png")
    #bg_image = Image.open("assets/gym_icon.png")
    bg_image = bg_image.resize((window.winfo_screenwidth(),window.winfo_screenheight()))  # Match your window size
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Set image as a label background
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    bg_label.image = bg_photo

