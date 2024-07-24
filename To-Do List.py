import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
import pymongo
import matplotlib.pyplot as plt

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
tasks_collection = db["tasks"]

def add_task():
    task = task_entry.get()
    date = date_entry.get_date()
    if task != "":
        formatted_date = date.strftime("%d/%m/%Y")
        task_info = {"task": task, "date": formatted_date}
        tasks_listbox.insert(tk.END, format_task(task_info))
        task_entry.delete(0, tk.END)
        date_entry.set_date(datetime.date.today())
        tasks_collection.insert_one(task_info)  # Insert task into MongoDB
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def remove_task():
    try:
        # Get selected task index
        selected_task_index = tasks_listbox.curselection()[0]
        task_str = tasks_listbox.get(selected_task_index)
        
        # Split the task string to get task and date
        task_parts = task_str.split(" - ")
        if len(task_parts) == 2:
            task = {"task": task_parts[0], "date": task_parts[1]}
            
            # Remove the task from the listbox
            tasks_listbox.delete(selected_task_index)
            
            # Remove the task from MongoDB
            result = tasks_collection.delete_one(task)
            if result.deleted_count == 0:
                messagebox.showwarning("Warning", "Task not found in the database.")
        else:
            messagebox.showwarning("Warning", "Task format is incorrect.")
    
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to remove.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def update_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        new_task = task_entry.get()
        new_date = date_entry.get_date()
        if new_task != "":
            task_str = tasks_listbox.get(selected_task_index)
            task_parts = task_str.split(" - ")
            old_task = {"task": task_parts[0], "date": task_parts[1]}
            tasks_listbox.delete(selected_task_index)
            formatted_date = new_date.strftime("%d/%m/%Y")
            new_task_info = {"task": new_task, "date": formatted_date}
            tasks_listbox.insert(selected_task_index, format_task(new_task_info))
            task_entry.delete(0, tk.END)
            date_entry.set_date(datetime.date.today())
            tasks_collection.update_one(old_task, {"$set": new_task_info})  # Update task in MongoDB
        else:
            messagebox.showwarning("Warning", "You must enter a new task.")
    except:
        messagebox.showwarning("Warning", "You must select a task to update.")

def format_task(task_info):
    return f"{task_info['task']} - {task_info['date']}"

def load_tasks():
    tasks = tasks_collection.find()
    for task in tasks:
        tasks_listbox.insert(tk.END, format_task(task))

def show_stats():
    # Get tasks from MongoDB
    tasks = tasks_collection.find()
    
    # Create a dictionary to count tasks per month
    monthly_tasks = {}
    for task in tasks:
        task_date = datetime.datetime.strptime(task["date"], "%d/%m/%Y")
        month_year = task_date.strftime("%Y-%m")
        if month_year in monthly_tasks:
            monthly_tasks[month_year] += 1
        else:
            monthly_tasks[month_year] = 1
    
    # Sort the dictionary by month
    sorted_months = sorted(monthly_tasks.keys())
    task_counts = [monthly_tasks[month] for month in sorted_months]

    # Plot the results
    plt.figure(figsize=(10, 5))
    plt.plot(sorted_months, task_counts, marker='o', linestyle='-', color='b')
    plt.xlabel('Month')
    plt.ylabel('Number of Tasks')
    plt.title('Number of Tasks per Month')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Create the main window
root = tk.Tk()
root.title("To-Do List")
root.geometry("500x650")
root.configure(bg="#2E3B4E")  # Dark Blue Background

# Create and place widgets
title_label = tk.Label(root, text="To-Do List", bg="#2E3B4E", fg="#FFFFFF", font=("Arial", 20))
title_label.pack(pady=10)

# Frame to hold task entry and date entry
entry_frame = tk.Frame(root, bg="#2E3B4E")
entry_frame.pack(pady=5)

task_entry = tk.Entry(entry_frame, width=20, font=("Arial", 14), bg="#FFFFFF", fg="#333333")  # White Background, Dark Text
task_entry.pack(side=tk.LEFT, padx=5)

date_entry = DateEntry(entry_frame, width=12, background='#2E3B4E', foreground='#FFFFFF', borderwidth=2, font=("Arial", 14), selectmode='day')
date_entry.set_date(datetime.date.today())  # Set default date to today for testing
date_entry.pack(side=tk.LEFT, padx=5)

# Frame to hold the buttons
button_frame = tk.Frame(root, bg="#2E3B4E")
button_frame.pack(pady=5)

button_width = 16

add_button = tk.Button(button_frame, text="Add Task", command=add_task, bg="#B39DDB", fg="black", font=("Arial", 12), width=button_width)  # Dark Pastel Lavender
add_button.pack(side=tk.LEFT, padx=5)

update_button = tk.Button(button_frame, text="Update Task", command=update_task, bg="#FFDAB9", fg="black", font=("Arial", 12), width=button_width)  # Dark Pastel Peach
update_button.pack(side=tk.LEFT, padx=5)

remove_button = tk.Button(button_frame, text="Remove Task", command=remove_task, bg="#A0D6B4", fg="black", font=("Arial", 12), width=button_width)  # Dark Pastel Mint
remove_button.pack(side=tk.LEFT, padx=5)

tasks_listbox = tk.Listbox(root, width=45, height=20, font=("Arial", 12), bg="#FFFFFF", fg="#333333")  # White Background, Dark Text
tasks_listbox.pack(pady=10)

stats_button = tk.Button(root, text="Show Stats", command=show_stats, bg="#FFB6C1", fg="black", font=("Arial", 12), width=button_width)  # Light Pink
stats_button.pack(pady=10)

# Load tasks on startup
load_tasks()

# Run the application
root.mainloop()
