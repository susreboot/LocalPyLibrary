import tkinter as tk
from tkinter import ttk
import os
import tkinter.font as font
from tkinter import *
import sqlite3
from datetime import datetime
from tkinter import messagebox


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

def display_issued_books(content_frame, header_label):
    # Create a new frame for the table
    table_frame = tk.Frame(content_frame, padx=5, pady=50)
    table_frame.pack(fill="x", expand=True)

    # Create a label for the table name
    table_name_label = tk.Label(table_frame, text="Issued Books", font=("Arial", 16, "bold"))
    table_name_label.pack(side="top", pady=10)

    # Connect to the database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Create a frame for the treeview
    tree_frame = tk.Frame(table_frame, borderwidth=0, padx=5, pady=5) # Updated padding value here
    tree_frame.pack(side="top", expand=True, fill="both")

    # Create the student table
    tree = ttk.Treeview(tree_frame, columns=("sname", "bookname", "subject", "issuedate", "expirydate"), show="headings")

    tree.heading("sname", text="Student Name", anchor="center")
    tree.column("sname", width=200, anchor="center", stretch=True)
    tree.heading("bookname", text="Book Name", anchor="center")
    tree.column("bookname", width=200, anchor="center", stretch=True)
    tree.heading("subject", text="Subject", anchor="center")
    tree.column("subject", width=200, anchor="center", stretch=True)
    tree.heading("issuedate", text="Issue Date", anchor="center")
    tree.column("issuedate", width=200, anchor="center", stretch=True)
    tree.heading("expirydate", text="Expiry Date", anchor="center")
    tree.column("expirydate", width=200, anchor="center", stretch=True)

    tree.pack(side="top", fill="both", expand=True)

    # Add the current issued books to the table
    book_cursor = conn.cursor()
    book_cursor.execute("SELECT bookid, bookname, subject FROM home_addbook WHERE bookid IN (SELECT book1 FROM home_issuebook)")
    book_data = book_cursor.fetchall()

    student_cursor = conn.cursor()
    student_cursor.execute("SELECT studentid, sname FROM home_addstudent")
    student_data = student_cursor.fetchall()

    issue_cursor = conn.cursor()
    issue_cursor.execute("SELECT studentid, book1, user_id, expirydate, issuedate FROM home_issuebook")
    issue_data = issue_cursor.fetchall()

    # Insert data into the treeview
    for data in issue_data:
        book1_data = next((book for book in book_data if book[0] == data[1]), None)
        student_data = next((student for student in student_data if student[0] == data[0]), None)
        if book1_data:
            tree.insert("", "end", values=(student_data[1], book1_data[1], book1_data[2], data[4], data[3]))

    # Close the database connection
    conn.close()

    return table_frame

def delete_selected_item(tree):
    cur_item = tree.focus()
    if cur_item:
        tree.delete(cur_item)

        # Update the database to delete the corresponding row
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM home_addbook WHERE id=?", (cur_item,))
        conn.commit()
        conn.close()

def display_books(content_frame, header_label):
    # Create a new frame for the table
    table_frame = tk.Frame(content_frame, padx=5, pady=5)
    table_frame.pack(fill="x", expand=True)
    
    # Create a label for the table name
    table_name_label = tk.Label(table_frame, text="Library Books", font=("Arial", 16, "bold"), highlightbackground="#212121", highlightcolor="#212121")
    table_name_label.pack(pady=10)

    # Connect to the database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Create a frame for the treeview
    tree_frame = tk.Frame(table_frame, borderwidth=0, padx=5, pady=5) # Updated padding value here
    tree_frame.pack(side="top", expand=True, fill="both")

    # Create the student table
    tree = ttk.Treeview(tree_frame, columns=("bookid", "bookname", "author", "subject", "status"), show="headings")
    tree.heading("bookid", text="Book ID", anchor="center")
    tree.column("bookid", width=100, anchor="center", minwidth=100, stretch=True)
    tree.heading("bookname", text="Book Name", anchor="center")
    tree.column("bookname", width=200, anchor="center", minwidth=200, stretch=True)
    tree.heading("subject", text="Subject", anchor="center")
    tree.column("subject", width=200, anchor="center", minwidth=200, stretch=True)
    tree.heading("status", text="Status", anchor="center")
    tree.column("status", width=200, anchor="center", minwidth=200, stretch=True)
    tree.heading("author", text="Author", anchor="center")
    tree.column("author", width=200, anchor="center", minwidth=200, stretch=True)


    
    tree.pack(side="top", fill="both", expand=True)

    # Add the current students to the table
    cursor.execute("SELECT * FROM home_addbook")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=(row[1], row[2], row[6], row[3], row[4]))

    conn.close()

    # Create a delete button
    delete_button = ttk.Button(table_frame, 
                               text="Delete Selected Book", 
                               command=lambda: delete_selected_item(tree)
                               )
    
    delete_button.pack(side="bottom", 
                       padx=10, 
                       pady=10
                       )
    
    edit_button = ttk.Button(table_frame, text="Edit Selected Book", command=lambda: edit_selected_item(tree))
    edit_button.pack(side="bottom", 
                       padx=10, 
                       pady=10
                       )

    def save_edited_item(tree, selected_item, book_id_entry, book_name_entry, author_entry, subject_entry, status_entry, edit_window):
        tree.item(selected_item, text="", values=(book_id_entry.get(), book_name_entry.get(), author_entry.get(), subject_entry.get(), status_entry.get()))
        edit_window.destroy()

    def edit_selected_item(tree):
        # Get the selected item from the treeview
        selected_item = tree.focus()[0]

        # Check if an item was selected
        if selected_item:
            # Get the values of the selected item
            item_values = tree.item(selected_item)['values']
            
            # Create a new window for editing the selected item
            edit_window = tk.Toplevel()
            edit_window.title("Edit Book")

            # Calculate the x and y coordinates to center the window on the screen
            screen_width = edit_window.winfo_screenwidth()
            screen_height = edit_window.winfo_screenheight()
            window_width = 250
            window_height = 250
            x = (screen_width/2) - (window_width/2)
            y = (screen_height/2) - (window_height/2)

            # Set the dimensions and position of the window
            edit_window.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
            
            # Create labels and entry fields for each column in the table
            book_id_label = tk.Label(edit_window, text="Book ID:")
            book_id_label.grid(row=0, column=0, padx=5, pady=5)
            book_id_entry = tk.Entry(edit_window)
            book_id_entry.grid(row=0, column=1, padx=5, pady=5)
            book_id_entry.insert(0, item_values[0])

            book_name_label = tk.Label(edit_window, text="Book Name:")
            book_name_label.grid(row=1, column=0, padx=5, pady=5)
            book_name_entry = tk.Entry(edit_window)
            book_name_entry.grid(row=1, column=1, padx=5, pady=5)
            book_name_entry.insert(0, item_values[1])

            author_label = tk.Label(edit_window, text="Author:")
            author_label.grid(row=2, column=0, padx=5, pady=5)
            author_entry = tk.Entry(edit_window)
            author_entry.grid(row=2, column=1, padx=5, pady=5)
            author_entry.insert(0, item_values[2])

            subject_label = tk.Label(edit_window, text="Subject:")
            subject_label.grid(row=3, column=0, padx=5, pady=5)
            subject_entry = tk.Entry(edit_window)
            subject_entry.grid(row=3, column=1, padx=5, pady=5)
            subject_entry.insert(0, item_values[3])

            status_label = tk.Label(edit_window, text="Status:")
            status_label.grid(row=4, column=0, padx=5, pady=5)
            status_entry = tk.Entry(edit_window)
            status_entry.grid(row=4, column=1, padx=5, pady=5)
            status_entry.insert(0, item_values[4])

            # Create a button to save the changes
            save_button = tk.Button(edit_window, text="Save Changes", command=lambda: save_edited_item(tree, selected_item, book_id_entry, book_name_entry, author_entry, subject_entry, status_entry))
            save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

            # Return the edit window object
            return edit_window

        else:
            # If no item was selected, display an error message
            messagebox.showerror("Error", "No item selected.")


    # Return the table frame
    return table_frame


def display_patrons(content_frame, header_label):
    # Create a new frame for the table
    table_frame = tk.Frame(content_frame, bd=2, padx=20, pady=10)
    table_frame.pack(fill="x", expand=True)
    
    # Create a label for the table name
    table_name_label = tk.Label(table_frame, text="Library Patrons", font=("Arial", 16, "bold"))
    table_name_label.pack(pady=10)

    # Connect to the database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Create a style for the treeview
    style = ttk.Style()
    style.theme_use("default")
    style.configure('Treeview', highlightthickness=0, bd=0, font=('Arial', 11))
    style.configure('Treeview.Heading', background='light blue', foreground='black', font=('Arial', 12, 'bold'))
    style.layout('Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])
    style.configure('Treeview', rowheight=30, padding=0)

    # Create a frame for the treeview
    tree_frame = tk.Frame(table_frame, borderwidth=0, padx=5, pady=5) # Updated padding value here
    tree_frame.pack(side="top", expand=True, fill="both")

    # Create the student table
    tree = ttk.Treeview(tree_frame, columns=("Student ID", "Student Name"), show="headings", style="Treeview")
    
    tree.heading("Student ID", text="Student ID", anchor="center")
    tree.column("Student ID", width=100, anchor="center")
    tree.heading("Student Name", text="Student Name", anchor="center")
    tree.column("Student Name", width=200, anchor="center")
    tree.pack(side="top", fill="both", expand=True)

    # Add the current students to the table
    cursor.execute("SELECT * FROM home_addstudent")
    rows = cursor.fetchall()
    for i, row in enumerate(rows):
        if i % 2 == 0:
            tree.insert("", tk.END, values=(row[2], row[1]), tags=('evenrow',))
        else:
            tree.insert("", tk.END, values=(row[2], row[1]), tags=('oddrow',))

    conn.close()

    # Define the even and odd row styles
    style.configure('Treeview', rowheight=30)
    style.configure('Treeview.EvenRow', background='#F2F2F2')
    style.configure('Treeview.OddRow', background='white')

    # Add the row styles to the table
    style.map('Treeview.Heading', background=[('active', 'light blue')])

    tree.tag_configure('evenrow', background='#F2F2F2')
    tree.tag_configure('oddrow', background='white')

    # Return the table frame
    return table_frame


def dashboard(content_frame, header_label):
    # Clear the content frame before adding new widgets
    clear_content_frame(content_frame)

    # Change the header label
    header_label.config(text="Dashboard")

    # Create a canvas widget inside the content frame
    canvas = tk.Canvas(content_frame, bg="#FFFFFF", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar to the canvas widget
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Link the scrollbar to the canvas widget
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas widget to hold the dashboard widgets
    dashboard_frame = tk.Frame(canvas, bd=2, relief=tk.SOLID, pady=10)
    canvas.create_window((0, 0), window=dashboard_frame, anchor="nw", tags="dashboard_frame")

    # Add the dashboard widgets to the dashboard frame
    dashboard_header = tk.Label(dashboard_frame, text="DASHBOARD", font=("Arial", 24, "bold"), pady=10)
    dashboard_header.pack()

    display_books(dashboard_frame, header_label)

    display_patrons(dashboard_frame, header_label)

    display_issued_books(dashboard_frame, header_label)

    # Set the canvas scrolling region
    def resize_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", resize_canvas)

    # Bind mouse wheel event to canvas
    canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    content_frame.update_idletasks()

    # Configure canvas to scroll on mouse wheel event
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Resize the canvas scroll region to fit the dashboard frame
    canvas.itemconfig("dashboard_frame", width=canvas.winfo_width())

    # Update canvas size to fit the parent window size
    def resize_canvas_parent(event):
        canvas.configure(width=event.width, height=event.height)
        canvas.itemconfig("dashboard_frame", width=event.width)

    canvas.bind("<Configure>", resize_canvas_parent)


    
def add_book(content_frame, header_label):
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Book Management")

    books_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    books_frame.pack(fill="both", expand=True)

    books_header = tk.Label(books_frame, text="ADD BOOKS", font=("Arial", 24, "bold"), pady=10)
    books_header.pack()

    # Create a form to add a new book
    add_book_form = tk.Frame(books_frame, pady=10)
    add_book_form.pack()

    # Create labels and entry fields for book title, author, subject, and status
    bookid_label = tk.Label(add_book_form, text="ISBN", font=("Arial", 16))
    bookid_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    bookid_entry = tk.Entry(add_book_form, font=("Arial", 16))
    bookid_entry.grid(row=0, column=1, padx=10, pady=5)
    
    title_label = tk.Label(add_book_form, text="Title", font=("Arial", 16))
    title_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    title_entry = tk.Entry(add_book_form, font=("Arial", 16))
    title_entry.grid(row=1, column=1, padx=10, pady=5)

    author_label = tk.Label(add_book_form, text="Author", font=("Arial", 16))
    author_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    author_entry = tk.Entry(add_book_form, font=("Arial", 16))
    author_entry.grid(row=2, column=1, padx=10, pady=5)

    subject_label = tk.Label(add_book_form, text="Subject", font=("Arial", 16))
    subject_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    subject_entry = tk.Entry(add_book_form, font=("Arial", 16))
    subject_entry.grid(row=3, column=1, padx=10, pady=5)

        
    # Create a function to handle form submission
    def add_book_submit():
        # Get the values of the form fields
        bookid = bookid_entry.get()
        title = title_entry.get()
        author = author_entry.get()
        subject = subject_entry.get()

        # Add the new book to the database
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO home_addbook (bookid, bookname, subject, author, status, user_id) VALUES (?, ?, ?, ?, 'NOT-ISSUED', ?)", (bookid, title, subject, author, logged_user))
            conn.commit()
            messagebox.showinfo("Success", "Book added successfully")
            conn.close()
            add_book(content_frame, header_label)
        except:
            messagebox.showerror("Error", "Could not add book to database")
        conn.close()

    # Clear the form fields after submission
    bookid_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)

    # Add a submit button to the form
    logged_user = 5
    submit_button = tk.Button(add_book_form, text="Submit", font=("Arial", 16), command=add_book_submit)
    submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Show the current books
    display_books(content_frame, header_label)
    
    #Show the current Patrons
    display_patrons(content_frame, header_label)


def view_patrons(content_frame, header_label):
    clear_content_frame(content_frame)
    # Change the header label
    header_label.config(text="Patrons Report")
    # Create the view patrons frame
    view_patrons_frame = tk.Frame(content_frame, bd=2, relief=tk.SOLID, padx=20, pady=10)
    view_patrons_frame.pack(fill="both", expand=True)

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
    add_patron_frame.pack(fill="both", expand=True)

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
    
welcome(header_frame, header_label)

root.mainloop()