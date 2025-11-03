from tkinter import PhotoImage, Tk


def c_icon(window: Tk ):

    photo = PhotoImage(file = "assets/gym_icon.png")  # Placeholder for the logo path
    window.iconphoto(True, photo) #Set the icon for the main window
