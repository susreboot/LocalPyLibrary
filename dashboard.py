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
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Create the sidenav
    sidenav_frame = create_nav(root, content_frame, header_label)
    sidenav_frame.pack(side=tk.LEFT, fill=tk.Y)
    
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
    date_label.pack(side="top", fill="x", padx=10, pady=10)
    date_label.place(relx=1, x=-10, y=10, anchor="ne")


    logo_image = tk.PhotoImage(file='logo.png')
    logo_label = tk.Label(sidenav_frame, image=logo_image)
    logo_label.pack(pady=10)
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

    for item in nav_items:
        button = Button(sidenav_frame, text=item[0], font=("Arial", 14), bg="#2b2b2b", fg="white", bd=0, compound=LEFT, padx=10, pady=10, relief="flat", command=item[1])
        button.pack(side=TOP, fill=X, padx=10, pady=5)

    return sidenav_frame

def display_books(dashboard_frame):
    # Clear the dashboard frame before adding new widgets
    clear_content_frame(dashboard_frame)
    # Create a header label
    header_label = Label(dashboard_frame, text="LIBRARY BOOKS", font=("Arial", 24))
    header_label.pack(side='top', pady=20)
    # Connect to the database
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    # Execute the SELECT statement and retrieve the data
    c.execute(f"SELECT bookid, bookname, subject, status FROM home_addbook")
    data = c.fetchall()

    # Get the column names and data types
    names = [description[0] for description in c.description]
    types = [description[1] for description in c.description]

    # Create the table
    table = tk.Frame(dashboard_frame, bg='#00a6cc')
    table.pack(side='top', padx=20, pady=20)

    # Create a header row with the column names
    header_row = tk.Frame(table, bg='#1C6EA4')
    header_row.pack(side='top', fill='x', pady=5)
    for i, name in enumerate(names):
        # table.columnconfigure(i, weight=1)
        header_label = tk.Label(header_row, text=name, bg='#1C6EA4', fg='white', font=('Arial', 12, 'bold'), width=20, anchor='w')
        header_label.pack(side='left', padx=(5, 0), pady=5, fill='both', expand=True)

    # Create a data row for each row of data
    for i, row in enumerate(data):
        data_row = tk.Frame(table, bg='white')
        data_row.pack(side='top', fill='x', expand=True)
        for j, value in enumerate(row):
            data_label = tk.Label(data_row, text=value, bg='white', font=('Arial', 12), width=20, anchor='w')
            data_label.grid(row=i+1, column=j, sticky='news'+'e', padx=5, pady=5)
            if i % 2 == 0:
                data_label.configure(bg='#D0E4F5')
            else:
                data_label.configure(bg='#FFFFFF')
            # Add weight to each column
            table.columnconfigure(j, weight=1)
    # Add weight to each row
    table.rowconfigure(i+1, weight=1)

    # Close the database connection
    conn.close()

    # Set the style for the table
    style = ttk.Style()
    style.theme_use('default')
    style.configure('blueTable.TFrame', borderwidth=1, relief='solid', background='#00a6cc')
    style.configure('blueTable.TLabel', borderwidth=1, relief='solid', font=('Arial', 12), background='#FFFFFF', foreground='black', width=20)
    style.configure('blueTable.THeader', borderwidth=1, relief='solid', font=('Arial', 12, 'bold'), background='#1C6EA4', foreground='white', width=20)
    style.configure('blueTable.TFooter', borderwidth=1, relief='solid', font=('Arial', 12, 'bold'), background='#D0E4F5', foreground='black')
    style.map('blueTable.TLabel', background=[('alternate', '#D0E4F5'), ('selected', '#1C6EA4')])
    
    # Apply the style to the table
    table.configure(**style.configure('blueTable.TFrame'))
    for child in table.winfo_children():
        child.configure(**style.configure('blueTable.TLabel'))
        if child != header_row:
            child.grid_configure(sticky="news")
    header_row.configure(style='blueTable.THeader')
    for child in header_row.winfo_children():
        child.configure(style='blueTable.THeader')
    table.grid_columnconfigure(0, weight=1)
    table.winfo_children()[-1].configure(style='blueTable.TFooter')

def dashboard(content_frame, header_label):
    # Clear the content frame before adding new widgets
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Dashboard")
    
    dashboard_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    dashboard_frame.pack(pady=20)

    dashboard_header = tk.Label(dashboard_frame, text="DASHBOARD", font=("Arial", 24, "bold"), pady=10)
    dashboard_header.pack()

    # Call the display_books() function and pass the dashboard_frame to it
    display_books(dashboard_frame)
   
    
def add_book(content_frame, header_label):
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Book Management")

    books_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    books_frame.pack(pady=20)

    books_header = tk.Label(books_frame, text="ADD BOOKS", font=("Arial", 24, "bold"), pady=10)
    books_header.pack()

    books_table = tk.Label(books_frame, text="TODO: BOOK STUFF HERE", font=("Arial", 16))
    books_table.pack()
    
    # TODO: Add code to display books table

    # Add book form elements here

def view_patrons(content_frame, header_label):
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Patrons Report")
    # Create the view patrons frame
    view_patrons_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    view_patrons_frame.pack(pady=20)

    # Create the view patrons header
    view_patrons_header = tk.Label(view_patrons_frame, text="VIEW PATRONS", font=("Arial", 24, "bold"), pady=10)
    view_patrons_header.pack()
    
    view_patrons_table = tk.Label(view_patrons_frame, text="TODO: PATRON VIEW STUFF HERE", font=("Arial", 16))
    view_patrons_table.pack()

    # TODO: Add code to display patrons table

def add_patron(content_frame, header_label):
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Patron Management") 
    
    add_patron_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    add_patron_frame.pack(pady=20)

    add_patron_header = tk.Label(add_patron_frame, text="ADD PATRON", font=("Arial", 24, "bold"), pady=10)
    add_patron_header.pack()
    
    add_patron_table = tk.Label(add_patron_frame, text="TODO: Patron STUFF HERE", font=("Arial", 16))
    add_patron_table.pack()

def view_issued_books(content_frame, header_label):
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Issued Books Report")
    
    issued_books_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    issued_books_frame.pack(pady=20)

    issued_books_header = tk.Label(issued_books_frame, text="ISSUED BOOKS", font=("Arial", 24, "bold"), pady=10)
    issued_books_header.pack()
    
    issued_books_table = tk.Label(issued_books_frame, text="TODO: BOOK STUFF HERE", font=("Arial", 16))
    issued_books_table.pack()

    # View issued books table here
    
def issue_book(content_frame, header_label):
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Issue Books")
    
    issue_book_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    issue_book_frame.pack(pady=20)

    issue_book_header = tk.Label(issue_book_frame, text="ISSUE BOOK", font=("Arial", 24, "bold"), pady=10)
    issue_book_header.pack()
    
    issue_book_table = tk.Label(issue_book_frame, text="TODO: BOOK STUFF HERE", font=("Arial", 16))
    issue_book_table.pack()

    # Issue book form elements here

def return_book(content_frame, header_label):
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Return Books")
    
    return_book_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    return_book_frame.pack(pady=20)

    return_book_header = tk.Label(return_book_frame, text="RETURN BOOK", font=("Arial", 24, "bold"), pady=10)
    return_book_header.pack()
    
    return_book_table = tk.Label(return_book_frame, text="TODO: BOOK STUFF HERE", font=("Arial", 16))
    return_book_table.pack()

    # Return book form elements here
    

def log_out():
    root.destroy()
    
root = tk.Tk()
root.geometry("1920x1080")
root.title("Library Management System")
# Maximize the window
root.state('zoomed')

header_frame = tk.Frame(root, bg="#212121", padx=20, pady=10)
header_frame.pack(fill=tk.X)

header_label = tk.Label(header_frame, text="WELCOME", font=("Arial", 24, "bold"), fg="black", padx=10)
header_label.pack(side=tk.LEFT)
    
welcome(content_frame, header_label)

root.mainloop()