import tkinter as tk
import tkinter.font as font
import os
import sqlite3
from datetime import datetime
from tkinter import ttk
from tkinter import Button
from tkinter import *

content_frame = None

def clear_content_frame(frame):
    """
    This function clears the content frame by destroying all the widgets inside it.
    """
    if frame is not None:
        for widget in frame.winfo_children():
            widget.destroy()

def welcome(content_frame, header_label):
    """
    This function displays the welcome screen of the application.
    """
    # Create the main content area
    content_frame = tk.Frame(root, padx=20, pady=10)
    content_frame.grid(row=1, column=1, sticky="nsew")
    root.columnconfigure(1, weight=1) 

    # Create the sidenav
    sidenav_frame = create_nav(root, content_frame, header_label)
    sidenav_frame.grid(row=0, column=0, sticky="nsew")
    root.rowconfigure(1, weight=1)

    books_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    books_frame.grid(row=0, column=0, pady=20)

    books_header = tk.Label(books_frame, text="Welcome to the Library", font=("Arial", 24, "bold"), pady=10)
    books_header.pack()

    books_table = tk.Label(books_frame, text="TODO: ADD MESSAGE", font=("Arial", 16))
    books_table.pack()

def create_nav(root, content_frame, header_label):
    
    sidenav_frame = Frame(root, bg="#2b2b2b", padx=10, pady=10)
    sidenav_frame.grid_columnconfigure(0, weight=1)
    # Create a label to display the date and time
    date_label = tk.Label(root, text=f"Date: {datetime.now().strftime('%m-%d-%Y')}   Time: {datetime.now().strftime('%I:%M %p')}", font=("Arial", 12), anchor="e")

    # Define a function to update the date and time label
    def update_date_label():
        date_label.config(text=f"Date: {datetime.now().strftime('%m-%d-%Y')}   Time: {datetime.now().strftime('%I:%M %p')}")
        date_label.after(1000, update_date_label)

    # Schedule the first update of the date and time label
    date_label.after(0, update_date_label)

    # Place the label in the top right corner of the window
    date_label.grid(row=0, column=1, sticky="e", padx=10, pady=10)
    date_label.place(relx=1, x=-10, y=10, anchor="ne")


    logo_image = tk.PhotoImage(file='logo.png')
    logo_label = tk.Label(sidenav_frame, image=logo_image)
    logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    logo_label.image = logo_image
    # configure the label to behave like a hyperlink
    logo_label.bind("<Button-1>", lambda event: dashboard(content_frame, header_label))

    logo_label.config(cursor="hand2", fg="blue", font=("Arial", 12, "underline"))

    font_path = os.path.join(os.getcwd(), "fonts", "fontawesome-webfont.ttf")
    fontawesome = font.Font(family="FontAwesome")
    # Create list of menu items with Font Awesome icons
    nav_items = [
        ("Dashboard", lambda: dashboard(content_frame, header_label)),
        ("Book Management", lambda: add_book(content_frame, header_label)),
        ("Patrons Report", lambda: view_patrons(content_frame, header_label)),
        ("Patron Management", lambda: add_patron(content_frame, header_label)),
        ("Issued Books Report", lambda: view_issued_books(content_frame, header_label)),
        ("Issue Book", lambda: issue_book(content_frame, header_label)),
        ("Return Book", lambda: return_book(content_frame, header_label)),
        ("Log Out", log_out), 
    ]

    for i, item in enumerate(nav_items):
        button = tk.Button(sidenav_frame, text=item[0], font=("Arial", 14), bg="#2b2b2b", fg="white", bd=0, compound=tk.LEFT, padx=10, pady=10, relief="flat", command=item[1])
        button.grid(row=i+1, column=0, sticky="ew", padx=10, pady=5)

    return sidenav_frame

def display_patrons(content_frame, header_label):
    header_label.config(text="PATRONS")
    
    # Create a new frame for the table
    table_frame = tk.Frame(content_frame)
    table_frame.grid(row=1, column=0, sticky="nsew")

    # Connect to the database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Create the student table
    tree = ttk.Treeview(table_frame, columns=("Student ID", "Student Name"), show="headings")
    tree.heading("Student ID", text="Student ID")
    tree.heading("Student Name", text="Student Name")
    tree.pack(expand=True, fill='both')

    # Add the current students to the table
    cursor.execute("SELECT * FROM home_addstudent")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=(row[2], row[1]))

    conn.close()

    # Return the table frame
    return table_frame

def dashboard(content_frame, header_label):
     # Clear the content frame before adding new widgets
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Dashboard")
    
    dashboard_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    dashboard_frame.grid(row=0, column=0, pady=20, sticky="nsew")
    
    dashboard_header = tk.Label(dashboard_frame, text="DASHBOARD", font=("Arial", 24, "bold"), pady=10)
    dashboard_header.place(relx=0.5, rely=0.5, anchor="center")
    dashboard_header.columnconfigure(0, weight=1)

    # Call the display_books() function and pass the dashboard_frame to it
    # display_books(dashboard_frame)
    table_frame = display_patrons(content_frame, header_label)

    display_patrons(table_frame)
    
def log_out():
    root.destroy()

root = tk.Tk()
root.geometry("1920x1080")
root.title("Library Management System")
# Maximize the window
root.state('zoomed')

header_frame = tk.Frame(root, bg="#212121", padx=20, pady=10)
header_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)

# Add a label to the header frame
header_label = tk.Label(header_frame, text="WELCOME", fg="#212121", font=("Helvetica", 18))
header_label.pack(pady=20)
# Create sidenav frame and add it to the grid
sidenav_frame = tk.Frame(root, bg="#757575", padx=10, pady=10)
sidenav_frame.grid(row=1, column=0, sticky="ns")

# # Add a label to the sidenav frame
# sidenav_label = tk.Label(sidenav_frame, text="Side Nav", fg="white", font=("Helvetica", 14))
# sidenav_label.pack()

# Create main content frame and add it to the grid
content_frame = tk.Frame(root, bg="#EEEEEE", padx=20, pady=10)
content_frame.grid(row=1, column=1, sticky="nsew")

# # Add a label to the content frame
# content_label = tk.Label(content_frame, text="Main Content", font=("Helvetica", 14))
# content_label.pack()

# Configure the grid to stretch the content frame horizontally and vertically
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

welcome(content_frame, header_label)

root.mainloop()