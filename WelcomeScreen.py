from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os

root = Tk()
root.title("Real-Time Language Translator")

height = 350
width = 800
x = (root.winfo_screenwidth()//2)-(width//2)
y = (root.winfo_screenheight()//2)-(height//2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
root.resizable(False, False)
root.overrideredirect(True)

my_img = ImageTk.PhotoImage(Image.open("RTLTWS.png"))
my_label = Label(image=my_img)
my_label.pack()

def open_new_window():
    root.withdraw()
    os.system("HomeScreen.py")
    root.destroy()
    
start_button = Button(root, text="Tap to Start →", font=('Arial', 14), command=open_new_window, borderwidth=0)
start_button.place(x=330, y=170)

# root.resizable(False, False)
root.mainloop()

