import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image

import pyttsx3
import googletrans
from tkinter import ttk, messagebox

root = tk.Tk()
root.title('Realtime language translator')
root.iconbitmap('translate.png')

w = 1010
h = 630
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (w/2)
y = (screen_height/2) - (h/2)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

# Load and resize the background image
bg_image = Image.open("RTLTHS.png")  # Replace with your image file path
resized_bg = bg_image.resize((w, h), Image.LANCZOS)  # Resize to the window dimensions
bg_photo = ImageTk.PhotoImage(resized_bg)

# Create a label to display the background image
bg_label = Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Set the image to cover the entire window

root.resizable(False, False)
root.overrideredirect(True)

recent_translations = []  # List to store recent translations

def show_recent_translations():
    recent_window = tk.Toplevel(root)
    recent_window.title("")
    recent_window.iconbitmap('recent.ico')
    recent_window.geometry("800x450")

    # Create a frame to hold the recent translations
    recent_frame = tk.Frame(recent_window, bg="#1980ff")
    recent_frame.pack(fill="both", expand=True)

    # Create a label to display the recent translations
    recent_label = tk.Label(recent_frame, text="Recent Translations", bg="#1980ff", fg="white", relief="ridge", font=("Helvetica", 16, "bold"))
    recent_label.pack(pady=10)

    # Create a text box to display the recent translations
    recent_text = tk.Text(recent_frame, height=17, width=80, relief="ridge", font=("Arial", 13))
    recent_text.pack(pady=10)

    # Create a clear all button
    clear_button = tk.Button(recent_frame, text="Clear All", image=new_clear, font="Arial, 15", command=lambda: recent_text.delete("1.0", "end"), compound="left")
    clear_button.pack( padx=105, pady=10)

    # Insert the recent translations into the text box
    for translation in recent_translations:
        recent_text.insert("end", f"Original: {translation['original']}\nTranslation: {translation['translation']}\n\n")

def on_enter(event):
    translate_button.config(bg="#1968e6")  # Change color on hover

def on_leave(event):
    translate_button.config(bg="#1980ff")  # Reset color when leaving
        
def minimize_window():
    root.wm_iconify()

def talk():
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 145)
        text_to_speak = original_text.get("1.0", END)
        engine.say(text_to_speak)
        engine.runAndWait()
        
    except Exception as e:
        messagebox.showerror("Failed to speak text")

def translate_it():
    translated_text.delete("1.0", END)  # Clear previous translation
    
    # Initialize translation to avoid UnboundLocalError
    translation = None
    
    try:
        # Fetch the language codes based on the selected languages
        for key, value in googletrans.LANGUAGES.items():
            if value == original_combo.get().lower():
                from_language_key = key
            if value == translated_combo.get().lower():
                to_language_key = key

        translator = googletrans.Translator()
        # Get the text to translate, strip extra whitespace
        text_to_translate = original_text.get("1.0", END).strip()
        
        # Perform translation
        translation = translator.translate(text_to_translate, src=from_language_key, dest=to_language_key)
        
        # Display the translation
        translated_text.insert("1.0", translation.text)

    except Exception as e:
        messagebox.showerror("Translator", str(e))
    
    if translation is not None:
        # Add the recent translation to the history list
        recent_translations.append({"original": text_to_translate, "translation": translation.text})

        # Limit the number of recent translations to 200
        if len(recent_translations) > 200:
            recent_translations.pop(0)
            
# Add Image to recent_button       
history_img = Image.open('recent.png')
resized = history_img.resize((24, 24), Image.LANCZOS)
new_history = ImageTk.PhotoImage(resized)

# Create a button to show recent translations
recent_button = tk.Button(root, text="History", image=new_history, bg="#7dcae6", fg="black", font=('Helvetica', 15, 'bold'), borderwidth=0, relief="solid", padx=7, command=show_recent_translations, compound="left")
recent_button.place(x=443, y=420)
  
#grab language list from googletrans
languages = googletrans.LANGUAGES

#convert to list
language_list = list(languages.values())
language_list = [value.upper() for value in language_list]

#text labels
# Create a custom font
custom_font = tkFont.Font(family="Poppins", size=18, weight="bold") 

label1 = tk.Label(root, text="Language Translator", fg="white", bg="#1980ff", font=('Helvetica', 16, 'bold'), padx=420, pady=5, borderwidth=5, relief="ridge").place(x=0, y=0)

image = Image.open("translate.png")
resized = image.resize((30, 30), Image.LANCZOS)
photo = ImageTk.PhotoImage(resized)

label = Label(root, image=photo, bg="#1980ff").place(x=393, y=5)

#tk.Label(root, text="Enter Text", fg="white", bg="#375c73", font=custom_font, padx=20).place(x=170, y=65)
#tk.Label(root, text="Translation", fg="#404040", bg="#b4eeb9", font=custom_font, padx=20).place(x=675, y=65)
tk.Label(root, text="Enter Text", fg="black", bg="#b5cae6", font=custom_font, padx=20).place(x=170, y=65)
tk.Label(root, text="Translation", fg="black", bg="#b5cae6", font=custom_font, padx=20).place(x=675, y=65)

#text boxes
original_text = Text(root, height=8, width=36, borderwidth=0, font=("Arial", 14), wrap="word",
                     highlightthickness=2, highlightbackground="#ccc", highlightcolor="#ccc")
original_text.grid(row=0, column=0, pady=105, padx=50)

translated_text = Text(root, height=8, width=36, borderwidth=0, font=("Arial", 14), wrap="word",
                     highlightthickness=2, highlightbackground="#ccc", highlightcolor="#ccc")
translated_text.grid(row=0, column=2, pady=105, padx=50)

#Button
translate_img = Image.open('download.png')
resized = translate_img.resize((125, 55), Image.LANCZOS)
new_img = ImageTk.PhotoImage(resized)

translate_button = Button(root, image=new_img, text="Translate", fg="white", bg="#1980ff", font=("Helvetica", 16, 'bold'), borderwidth=0, command=translate_it)
translate_button.place(x=439, y=320)

translate_button.bind("<Enter>", on_enter)  # Bind hover event
translate_button.bind("<Leave>", on_leave)  # Bind leave event

# Add Image to my_button
audio_img = Image.open('audio.png')
resized = audio_img.resize((22, 22), Image.LANCZOS)
new_audio = ImageTk.PhotoImage(resized)

# Text to Speak
my_button = Button(root, text="Listen", font=('Helvetica', 9, 'bold'), image=new_audio, fg="white", bg="#2196F3", borderwidth=1, command=talk, compound="left", padx=12, relief="solid")
my_button.place(x=49, y=287)

# Add Image to clear_button
clear_img = Image.open('clear.png')
resized = clear_img.resize((22, 22), Image.LANCZOS)
new_clear = ImageTk.PhotoImage(resized)

# Create a clear all button
clear_button = Button(root, text="Clear All", font=('Helvetica', 9, 'bold'), image=new_clear, fg="white", bg="#F44336", borderwidth=1, command=lambda: original_text.delete("1.0", "end"), compound="left", padx=12, relief="solid")
clear_button.place(x=145, y=287)

# Add Image to clear_button
exit_img = Image.open('exit.png')
resized = exit_img.resize((34, 32), Image.LANCZOS)
new_exit = ImageTk.PhotoImage(resized)

# Create an exit button
exit_button = Button(root, image=new_exit, borderwidth=0,  bg="#1980ff", command=root.destroy)
exit_button.place(x=973, y=5)

#text labels
tk.Label(root, text="Select Language", fg="black", bg="#b5cae6", font=('Helvetica', 14, "bold"), padx=15).place(x=160, y=358)
tk.Label(root, text="Select Translation Language", fg="black", bg="#b5cae6", font=('Helvetica', 14, "bold"), padx=15).place(x=606, y=358)

#Combo Boxes
original_combo = ttk.Combobox(root, width=50, value=language_list)
original_combo.current()
original_combo.grid(row=1, column=0)

translated_combo = ttk.Combobox(root, width=50, values=language_list)
translated_combo.current()
translated_combo.grid(row=1, column=2, pady=0, padx=0)

# Context menu for original text box
def cut_original_text():
    original_text.clipboard_clear()
    original_text.clipboard_append(original_text.selection_get())
    original_text.delete("sel.first", "sel.last")

def copy_original_text():
    original_text.clipboard_clear()
    original_text.clipboard_append(original_text.selection_get())

def paste_original_text():
    try:
        original_text.insert("sel.first", original_text.clipboard_get())
    except tk.TclError:
        original_text.insert("end", original_text.clipboard_get())

original_menu = Menu(root, tearoff=0)
original_menu.add_command(label="Cut", command=cut_original_text)
original_menu.add_command(label="Copy", command=copy_original_text)
original_menu.add_command(label="Paste", command=paste_original_text)

def show_original_menu(event):
    original_menu.post(event.x_root, event.y_root)

original_text.bind("<Button-3>", show_original_menu)

# Context menu for translated text box
def cut_translated_text():
    translated_text.clipboard_clear()
    translated_text.clipboard_append(translated_text.selection_get())
    translated_text.delete("sel.first", "sel.last")

def copy_translated_text():
    translated_text.clipboard_clear()
    translated_text.clipboard_append(translated_text.selection_get())

def paste_translated_text():
    try:
        translated_text.insert("sel.first", translated_text.clipboard_get())
    except tk.TclError:
        translated_text.insert("end", translated_text.clipboard_get())

translated_menu = Menu(root, tearoff=0)
translated_menu.add_command(label="Cut", command=cut_translated_text)
translated_menu.add_command (label="Copy", command=copy_translated_text)
translated_menu.add_command(label="Paste", command=paste_translated_text)

def show_translated_menu(event):
    translated_menu.post(event.x_root, event.y_root)

translated_text.bind("<Button-3>", show_translated_menu)

root.mainloop()