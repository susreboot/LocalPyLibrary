import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Create the "home_addstudent" table if it doesn't already exist
cursor.execute('''CREATE TABLE IF NOT EXISTS home_addstudent
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   sname TEXT,
                   studentid INTEGER,
                   user_id INTEGER)''')

# Create the Tkinter window
root = tk.Tk()
root.title("Add Students")

# Create the student name label and entry
name_label = tk.Label(root, text="Student Name")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

# Create the student ID label and entry
id_label = tk.Label(root, text="Student ID")
id_label.grid(row=1, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=1, column=1)

# Create a function to add the student to the database
def add_student():
    name = name_entry.get()
    studentid = id_entry.get()
    if name != "" and studentid != "":
        cursor.execute('''INSERT INTO home_addstudent (sname, studentid, user_id)
                          VALUES (?, ?, ?)''', (name, studentid, 1))
        conn.commit()
        messagebox.showinfo("Success", "Student added to database")
        name_entry.delete(0, tk.END)
        id_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter both name and ID")

# Create the add student button
add_button = tk.Button(root, text="Add Student", command=add_student)
add_button.grid(row=2, column=0)

# Create the exit button
exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=2, column=1)

# Create the student table
tree = ttk.Treeview(root, columns=("Student ID", "Student Name"), show="headings")
tree.heading("Student ID", text="Student ID")
tree.heading("Student Name", text="Student Name")
tree.grid(row=3, column=0, columnspan=2)

# Add the current students to the table
cursor.execute("SELECT * FROM home_addstudent")
rows = cursor.fetchall()
for row in rows:
    tree.insert("", tk.END, values=(row[2], row[1]))

# Start the Tkinter main loop
root.mainloop()
