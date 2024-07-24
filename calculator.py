import tkinter as tk

# Function to handle button click
def button_click(event):
    global last_result, last_operator, last_operand
    current = entry_var.get()
    text = event.widget.cget("text")
    
    if text == "=":
        try:
            if current == "":
                result = last_result
            else:
                if last_operator and current == str(last_result):
                    result = eval(f"{last_result}{last_operator}{last_operand}")
                else:
                    if last_operator == "%":
                        operand1, operand2 = current.split("%")
                        result = (float(operand1) * float(operand2)) / 100
                    else:
                        result = eval(current)
                    last_operand = current.split(last_operator)[-1] if last_operator else None
            entry_var.set(result)
            last_result = None
            last_operator = None
            last_operand = None
        except Exception:
            entry_var.set("Error")
            last_result, last_operator, last_operand = None, None, None
    elif text == "AC":
        entry_var.set("")
        last_result, last_operator, last_operand = None, None, None
    elif text == "CE":
        entry_var.set(current[:-1])
    else:
        if last_result is not None and current == str(last_result):
            current = ""
        if text in "+-*/%":
            last_operator = text
        entry_var.set(current + text)

# Set up the main application window
root = tk.Tk()
root.title("Professional Calculator")
root.configure(bg='#1B2631')  # Very dark blue background

# Variable for the entry field
entry_var = tk.StringVar()

# Entry field for displaying input and results
entry = tk.Entry(root, textvariable=entry_var, font=('Arial', 24), bd=0, relief=tk.FLAT, justify='right', bg='#ABB2B9', fg='black')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=30, sticky="nsew")

# Configure the grid to make it responsive
root.grid_rowconfigure(0, weight=1)
for i in range(1, 6):
    root.grid_rowconfigure(i, weight=1)
for j in range(4):
    root.grid_columnconfigure(j, weight=1)

# Button labels and styles
buttons = [
    ["AC", "CE", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", "±"]
]

# Button colors
button_bg = "#5DADE2"  
button_fg = "#FFFFFF"  
button_active_bg = "#3498DB"  
special_button_bg = "#2874A6"  
special_button_fg = "#FFFFFF"  
special_button_active_bg = "#1F618D"  

# Create buttons and add them to the grid
for i, row in enumerate(buttons):
    for j, btn_text in enumerate(row):
        button = tk.Button(root, text=btn_text, font=('Arial', 18), bd=0, relief=tk.FLAT, 
                           bg=special_button_bg if btn_text in ["AC", "CE", "="] else button_bg, 
                           fg=special_button_fg if btn_text in ["AC", "CE", "="] else button_fg,
                           activebackground=special_button_active_bg if btn_text in ["AC", "CE", "="] else button_active_bg,
                           activeforeground=button_fg)
        button.grid(row=i+1, column=j, padx=5, pady=5, sticky="nsew")
        button.bind("<Button-1>", button_click)

# Initialize global variables
last_result, last_operator, last_operand = None, None, None

# Start the application
root.mainloop()
