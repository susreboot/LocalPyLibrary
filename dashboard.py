import tkinter as tk
import os
import tkinter.font as font
from tkinter import *

content_frame = None

def clear_content_frame(content_frame):
    """Clears all widgets from the content frame."""
    for widget in content_frame.winfo_children():
        widget.destroy()

def welcome(content_frame, header_label):
    # Create the header
    # header_frame = tk.Frame(root, bg="#212121", padx=20, pady=10)
    # header_frame.pack(fill=tk.X)

    # header_label = tk.Label(header_frame, text="WELCOME", font=("Arial", 24, "bold"), fg="black", padx=10)
    # header_label.pack(side=tk.LEFT)
    
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

    logo_image = tk.PhotoImage(file='logo.png')
    logo_label = tk.Label(sidenav_frame, image=logo_image)
    logo_label.pack(pady=10)
    logo_label.image = logo_image

    font_path = os.path.join(os.getcwd(), "fonts", "fontawesome-webfont.ttf")
    fontawesome = font.Font(family="FontAwesome")
    # Create list of menu items with Font Awesome icons
    nav_items = [
        ("Dashboard", lambda: dashboard(content_frame, header_label)),
        ("Add Book", lambda: add_book(content_frame, header_label)),
        ("View Patrons", view_patrons),
        ("Add Patron", add_patron),
        ("View Issued Books", view_issued_books),
        ("Issue Book", issue_book), 
        ("Return Book", return_book), 
        ("Log Out", log_out), 
    ]

    for item in nav_items:
        button = Button(sidenav_frame, text=item[0], font=("Arial", 14), bg="#2b2b2b", fg="white", bd=0, compound=LEFT, padx=10, pady=10, relief="flat", command=item[1])
        button.pack(side=TOP, fill=X, padx=10, pady=5)

    return sidenav_frame

def dashboard(content_frame, header_label):
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Dashboard")
    books_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    books_frame.pack(pady=20)

    books_header = tk.Label(books_frame, text="DASHBOARD", font=("Arial", 24, "bold"), pady=10)
    books_header.pack()

    books_table = tk.Label(books_frame, text="TODO: DASHBOARD STUFF HERE", font=("Arial", 16))
    books_table.pack()

def add_book(content_frame, header_label):
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Add Book")

    books_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    books_frame.pack(pady=20)

    books_header = tk.Label(books_frame, text="ADD BOOKS", font=("Arial", 24, "bold"), pady=10)
    books_header.pack()

    books_table = tk.Label(books_frame, text="TODO: BOOK STUFF HERE", font=("Arial", 16))
    books_table.pack()
    
    # TODO: Add code to display books table

    # Add book form elements here

def view_patrons():
    # Create the view patrons frame
    view_patrons_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    view_patrons_frame.pack(pady=20)

    # Create the view patrons header
    view_patrons_header = tk.Label(view_patrons_frame, text="VIEW PATRONS", font=("Arial", 24, "bold"), pady=10)
    view_patrons_header.pack()

    # TODO: Add code to display patrons table

def add_patron():
    content_frame = tk.Frame(root, padx=20, pady=10)
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)    
    
    add_patron_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    add_patron_frame.pack(pady=20)

    add_patron_header = tk.Label(add_patron_frame, text="ADD PATRON", font=("Arial", 24, "bold"), pady=10)
    add_patron_header.pack()

def view_issued_books():
    content_frame = tk.Frame(root, padx=20, pady=10)
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    issued_books_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    issued_books_frame.pack(pady=20)

    issued_books_header = tk.Label(issued_books_frame, text="ISSUED BOOKS", font=("Arial", 24, "bold"), pady=10)
    issued_books_header.pack()

    # View issued books table here
    
def issue_book():
    content_frame = tk.Frame(root, padx=20, pady=10)
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    issue_book_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    issue_book_frame.pack(pady=20)

    issue_book_header = tk.Label(issue_book_frame, text="ISSUE BOOK", font=("Arial", 24, "bold"), pady=10)
    issue_book_header.pack()

    # Issue book form elements here

def return_book():
    content_frame = tk.Frame(root, padx=20, pady=10)
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    return_book_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    return_book_frame.pack(pady=20)

    return_book_header = tk.Label(return_book_frame, text="RETURN BOOK", font=("Arial", 24, "bold"), pady=10)
    return_book_header.pack()

    # Return book form elements here
    

def log_out():
    root.destroy()
    
root = tk.Tk()
root.geometry("800x600")
root.title("Library Management System")

header_frame = tk.Frame(root, bg="#212121", padx=20, pady=10)
header_frame.pack(fill=tk.X)

header_label = tk.Label(header_frame, text="WELCOME", font=("Arial", 24, "bold"), fg="black", padx=10)
header_label.pack(side=tk.LEFT)
    
welcome(content_frame, header_label)

root.mainloop()