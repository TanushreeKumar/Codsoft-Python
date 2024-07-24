import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    try:
        length = int(length_entry.get())
        if length < 1:
            raise ValueError("Password length must be at least 1.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the length.")
        return

    characters = string.ascii_lowercase
    if uppercase_var.get():
        characters += string.ascii_uppercase
    if numbers_var.get():
        characters += string.digits
    if special_var.get():
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def generate_strong_password():
    try:
        length = int(length_entry.get())
        if length < 12:
            raise ValueError("Strong password should be at least 12 characters long.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the length.")
        return

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def copy_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(password_entry.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

def reset():
    length_entry.delete(0, tk.END)
    uppercase_var.set(False)
    numbers_var.set(False)
    special_var.set(False)
    password_entry.delete(0, tk.END)

# Create the main window
window = tk.Tk()
window.title("Password Generator")

background_color = "#2E2E2E"
text_color = "#FFFFFF"

# Create a frame for better organization
frame = tk.Frame(window, bg=background_color, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

# Labels and entries
tk.Label(frame, text="Password Length:", bg=background_color, font=("Arial", 12), fg=text_color).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
length_entry = tk.Entry(frame, font=("Arial", 12))
length_entry.grid(row=0, column=1, padx=10, pady=10)

# Checkboxes
uppercase_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Include Uppercase", variable=uppercase_var, bg=background_color, font=("Arial", 10), fg=text_color).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

numbers_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Include Numbers", variable=numbers_var, bg=background_color, font=("Arial", 10), fg=text_color).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

special_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Include Special Characters", variable=special_var, bg=background_color, font=("Arial", 10), fg=text_color).grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

button_bg = "#FF8C00"  
button_fg = "#000000"

generate_button = tk.Button(frame, text="Generate Password", command=generate_password, bg=button_bg, fg=button_fg, font=("Arial", 12, "bold"))
generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

strong_button = tk.Button(frame, text="Generate Strong Password", command=generate_strong_password, bg=button_bg, fg=button_fg, font=("Arial", 12, "bold"))
strong_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Password entry
tk.Label(frame, text="Generated Password:", bg=background_color, font=("Arial", 12), fg=text_color).grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)
password_entry = tk.Entry(frame, width=30, font=("Arial", 12))
password_entry.grid(row=6, column=1, padx=10, pady=10)

# Copy to clipboard and reset buttons
copy_button = tk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard, bg=button_bg, fg=button_fg, font=("Arial", 12, "bold"))
copy_button.grid(row=7, column=0, padx=10, pady=10)

reset_button = tk.Button(frame, text="Reset", command=reset, bg=button_bg, fg=button_fg, font=("Arial", 12, "bold"))
reset_button.grid(row=7, column=1, padx=10, pady=10)

# Make the window resizable
window.resizable(True, True)

window.mainloop()
