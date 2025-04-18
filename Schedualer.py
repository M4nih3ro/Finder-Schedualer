import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import datetime

class TaskScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Kinder Schedualer")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e2f')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                        background="#2c2c3e",
                        foreground="white",
                        fieldbackground="#2c2c3e",
                        rowheight=30,
                        font=('Segoe UI', 10))
        style.configure("Treeview.Heading", font=('Segoe UI', 12, 'bold'), background="#3e3e5e", foreground="white")
        
        style.configure("TButton",
                        font=('Segoe UI', 10, 'bold'),
                        padding=10,
                        relief="flat",
                        background="#3e8e41",
                        foreground="white")
        style.map("TButton",
                  background=[('active', '#4caf50')],
                  foreground=[('active', 'white')])

        self.tasks = []

        self.setup_ui()

    def setup_ui(self):
        top_frame = tk.Frame(self.root, bg='#1e1e2f')
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Task:", bg='#1e1e2f', fg='white', font=('Segoe UI', 10)).grid(row=0, column=0, padx=5)
        self.task_entry = ttk.Entry(top_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="Date:", bg='#1e1e2f', fg='white', font=('Segoe UI', 10)).grid(row=0, column=2, padx=5)
        self.date_entry = DateEntry(top_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=3, padx=5)

        tk.Label(top_frame, text="Time (HH:MM):", bg='#1e1e2f', fg='white', font=('Segoe UI', 10)).grid(row=0, column=4, padx=5)
        self.time_entry = ttk.Entry(top_frame, width=10)
        self.time_entry.grid(row=0, column=5, padx=5)

        add_btn = ttk.Button(top_frame, text="Add Task", command=self.add_task, style="TButton")
        add_btn.grid(row=0, column=6, padx=10)

        # Task display area
        self.tree = ttk.Treeview(self.root, columns=("Task", "Date", "Time"), show='headings')
        self.tree.heading("Task", text="Task")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.pack(pady=20, padx=10, fill='both', expand=True)

        # Buttons
        btn_frame = tk.Frame(self.root, bg='#1e1e2f')
        btn_frame.pack(pady=10)

        delete_btn = ttk.Button(btn_frame, text="Delete Task", command=self.delete_task, style="TButton")
        delete_btn.grid(row=0, column=0, padx=10)

        save_btn = ttk.Button(btn_frame, text="Save Tasks", command=self.save_tasks, style="TButton")
        save_btn.grid(row=0, column=1, padx=10)

        load_btn = ttk.Button(btn_frame, text="Load Tasks", command=self.load_tasks, style="TButton")
        load_btn.grid(row=0, column=2, padx=10)

    def add_task(self):
        task = self.task_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()

        if not task or not time:
            messagebox.showerror("Input Error", "Task and time must be filled out.")
            return

        self.tree.insert('', 'end', values=(task, date, time))
        self.tasks.append({"task": task, "date": date, "time": time})
        self.task_entry.delete(0, 'end')
        self.time_entry.delete(0, 'end')

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select a task to delete.")
            return
        for item in selected:
            index = self.tree.index(item)
            self.tree.delete(item)
            del self.tasks[index]

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)
        messagebox.showinfo("Success", "Tasks saved successfully.")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
                for i in self.tree.get_children():
                    self.tree.delete(i)
                for task in self.tasks:
                    self.tree.insert('', 'end', values=(task["task"], task["date"], task["time"]))
            messagebox.showinfo("Success", "Tasks loaded successfully.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved tasks found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskScheduler(root)
    root.mainloop()
