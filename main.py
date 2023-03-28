import tkinter as tk
from tkinter import *
import sqlite3
from tkinter import ttk
import subprocess

def open_login_window():
    login_window = tk.Toplevel()
    login_window.title("Login Form")
    login_window.geometry("300x300")
    login_window.configure(bg="#1C2833")

    global login_username
    global login_password
    global message

    login_username = StringVar()
    login_password = StringVar()
    message = StringVar()

    Label(login_window, text="Login Form", bg="#0E6655", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    Label(login_window, text="Username:", bg="#1C2833", fg="white", font=("Arial", 12, "bold")).grid(row=1, column=0, pady=5)
    Entry(login_window, textvariable=login_username, bg="#1C2833", fg="white", font=("Arial", 12)).grid(row=1, column=1, pady=5)

    Label(login_window, text="Password:", bg="#1C2833", fg="white", font=("Arial", 12, "bold")).grid(row=2, column=0, pady=5)
    Entry(login_window, textvariable=login_password, show="*", bg="#1C2833", fg="white", font=("Arial", 12)).grid(row=2, column=1, pady=5)

    ttk.Button(login_window, text="Login", command=login, style="Green.TButton").grid(row=3, column=0, columnspan=2, pady=10)

    Label(login_window, text="", textvariable=message, bg="#1C2833", fg="white", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=10)

     # Center the login window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width - login_window.winfo_reqwidth()) / 2)
    y = int((screen_height - login_window.winfo_reqheight()) / 2)
    login_window.geometry("+{}+{}".format(x, y))
    
    # Return login window object
    return login_window


def login():
    # Getting form data
    username = login_username.get()
    password = login_password.get()

    # Applying empty validation
    if username == '' or password == '':
        message.set("Fill in all fields")
    else:
        # Open database
        conn = sqlite3.connect('db.sqlite3')

        # Select query
        cursor = conn.execute(f'SELECT * FROM auth_user WHERE username="{username}" AND password="{password}"')

        # Fetch data 
        if cursor.fetchone():
            message.set("Login Successful")
            
            open_dashboard()
        else:
            message.set("Wrong username or password")

def open_dashboard():
    subprocess.Popen(['python', 'dashboard.py'])
    login_window = open_login_window()
    login_window.withdraw()
    root.destroy()
    
# Create a hidden root window
root = tk.Tk()
root.withdraw() # hide the root window
open_login_window() # open the login form window
root.mainloop()
