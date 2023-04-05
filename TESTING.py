import tkinter as tk
from tkinter import ttk
import os
import tkinter.font as font
from tkinter import *
import sqlite3
from datetime import datetime


content_frame = None

def clear_content_frame(content_frame):
    if content_frame is not None:
        for widget in content_frame.winfo_children():
            widget.destroy()
        
def welcome(content_frame, header_label):
    # Create the main content area
    content_frame = tk.Frame(root, padx=20, pady=10)
    content_frame.grid(row=1, column=1, sticky="nsew")

    # Create the sidenav
    sidenav_frame = create_nav(root, content_frame, header_label)
    sidenav_frame.grid(row=1, column=0, sticky="ns")

    books_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    books_frame.pack(pady=20)

    books_header = tk.Label(books_frame, text="Welcome to the Library", font=("Arial", 24, "bold"), pady=10)
    books_header.pack()

    books_table = tk.Label(books_frame, text="TODO: ADD MESSAGE", font=("Arial", 16))
    books_table.pack()



def create_nav(parent, content_frame, header_label):
    sidenav_frame = Frame(parent, bg="#2b2b2b", padx=10, pady=10)

    # Create a label to display the date and time
    date_label = tk.Label(root, text=f"Date: {datetime.now().strftime('%m-%d-%Y')}   Time: {datetime.now().strftime('%I:%M %p')}", font=("Arial", 12), anchor="e")

    # Define a function to update the date and time label
    def update_date_label():
        date_label.config(text=f"Date: {datetime.now().strftime('%m-%d-%Y')}   Time: {datetime.now().strftime('%I:%M %p')}")
        date_label.after(1000, update_date_label)

    # Schedule the first update of the date and time label
    date_label.after(0, update_date_label)

    # Place the label in the top right corner of the window
    date_label.grid(row=0, column=1, sticky='e', padx=10, pady=10)

    logo_image = tk.PhotoImage(file='logo.png')
    logo_label = tk.Label(sidenav_frame, image=logo_image)
    logo_label.grid(row=1, column=0, pady=10)
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
        button = Button(sidenav_frame, text=item[0], font=("Arial", 14), bg="#2b2b2b", fg="white", bd=0, compound=LEFT, padx=10, pady=10, relief="flat", command=item[1])
        button.grid(row=i+2, column=0, sticky='ew', padx=10, pady=5)

    return sidenav_frame


def display_books(content_frame, header_label):
    header_label.config(text="PATRONS")

    # Create a new frame for the table
    table_frame = tk.Frame(content_frame)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Connect to the database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Create the student table
    tree = ttk.Treeview(table_frame, columns=("Book ID", "Book Name", "Subject", "Status"),  show="headings")
    tree.heading("Book ID", text="Book ID")
    tree.heading("Book Name", text="Book Name")
    tree.heading("Subject", text="Subject")
    tree.heading("Status", text="Status")
    tree.pack(fill="both", expand=True)

    # Add the current students to the table
    cursor.execute("SELECT bookid, bookname, subject, status FROM home_addbook")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=(row[2], row[1]))

    conn.close()
    
    # Return the table frame
    return table_frame

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
    dashboard_frame.grid(row=0, column=0, pady=20)

    dashboard_header = tk.Label(dashboard_frame, text="DASHBOARD", font=("Arial", 24, "bold"), pady=10)
    dashboard_header.grid(row=0, column=0)

    # Call the display_books() function and pass the dashboard_frame to it
    # display_books(dashboard_frame)
    
    display_patrons()
   
    
# def add_book(content_frame, header_label):
#     clear_content_frame(content_frame)
#     # Change the header label
#     header_label.config(text="Book Management")

#     books_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
#     books_frame.pack(pady=20)

#     books_header = tk.Label(books_frame, text="ADD BOOKS", font=("Arial", 24, "bold"), pady=10)
#     books_header.pack()

#     books_table = tk.Label(books_frame, text="TODO: BOOK STUFF HERE", font=("Arial", 16))
#     books_table.pack()
    
#     # TODO: Add code to display books table

#     # Add book form elements here

# def view_patrons(content_frame, header_label):
#     clear_content_frame(content_frame)
#     # Change the header label
#     header_label.config(text="Patrons Report")
#     # Create the view patrons frame
#     view_patrons_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
#     view_patrons_frame.pack(pady=20)

#     # Create the view patrons header
#     view_patrons_header = tk.Label(view_patrons_frame, text="VIEW PATRONS", font=("Arial", 24, "bold"), pady=10)
#     view_patrons_header.pack()
    
#     view_patrons_table = tk.Label(view_patrons_frame, text="TODO: PATRON VIEW STUFF HERE", font=("Arial", 16))
#     view_patrons_table.pack()

#     # TODO: Add code to display patrons table

# def add_patron(content_frame, header_label):
#     clear_content_frame(content_frame)
#     # Change the header label
#     header_label.config(text="Patron Management") 
    
#     add_patron_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
#     add_patron_frame.pack(pady=20)

#     add_patron_header = tk.Label(add_patron_frame, text="ADD PATRON", font=("Arial", 24, "bold"), pady=10)
#     add_patron_header.pack()
    
#     add_patron_table = tk.Label(add_patron_frame, text="TODO: Patron STUFF HERE", font=("Arial", 16))
#     add_patron_table.pack()

# def view_issued_books(content_frame, header_label):
#     clear_content_frame(content_frame)
#     # Change the header label
#     header_label.config(text="Issued Books Report")
    
#     issued_books_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
#     issued_books_frame.pack(pady=20)

#     issued_books_header = tk.Label(issued_books_frame, text="ISSUED BOOKS", font=("Arial", 24, "bold"), pady=10)
#     issued_books_header.pack()
    
#     issued_books_table = tk.Label(issued_books_frame, text="TODO: BOOK STUFF HERE", font=("Arial", 16))
#     issued_books_table.pack()

#     # View issued books table here
    
# def issue_book(content_frame, header_label):
#     clear_content_frame(content_frame)
#     # Change the header label
#     header_label.config(text="Issue Books")
    
#     issue_book_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
#     issue_book_frame.pack(pady=20)

#     issue_book_header = tk.Label(issue_book_frame, text="ISSUE BOOK", font=("Arial", 24, "bold"), pady=10)
#     issue_book_header.pack()
    
#     issue_book_table = tk.Label(issue_book_frame, text="TODO: BOOK STUFF HERE", font=("Arial", 16))
#     issue_book_table.pack()

#     # Issue book form elements here

# def return_book(content_frame, header_label):
#     clear_content_frame(content_frame)
#     # Change the header label
#     header_label.config(text="Return Books")
    
#     return_book_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
#     return_book_frame.pack(pady=20)

#     return_book_header = tk.Label(return_book_frame, text="RETURN BOOK", font=("Arial", 24, "bold"), pady=10)
#     return_book_header.pack()
    
#     return_book_table = tk.Label(return_book_frame, text="TODO: BOOK STUFF HERE", font=("Arial", 16))
#     return_book_table.pack()

#     # Return book form elements here
    

def log_out():
    root.destroy()
    
root = tk.Tk()
root.geometry("1920x1080")
root.title("Library Management System")
# Maximize the window
root.state('zoomed')

header_frame = tk.Frame(root, bg="#212121", padx=20, pady=10)
header_frame.grid(row=0, column=0, sticky="ew")

header_label = tk.Label(header_frame, text="WELCOME", font=("Arial", 24, "bold"), fg="black", padx=10)
header_label.grid(row=0, column=0, sticky="w")
    
welcome(content_frame, header_label)

root.mainloop()

