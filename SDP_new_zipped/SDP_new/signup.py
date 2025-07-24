import tkinter as tk
from tkinter import messagebox
from database import insert_user, check_email_unique
from PIL import Image, ImageTk

class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
    

        self.create_widgets()

    def create_widgets(self):
    # Set background color
        self.configure(bg="pale goldenrod")

    # Create other widgets on top of the background
        self.username_label = tk.Label(self, text="Username", font=("Helvetica", 14, "bold"), bg="pale goldenrod")
        self.username_label.grid(row=0, column=1, padx=10, pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=2, padx=10, pady=10)

        self.email_label = tk.Label(self, text="Email", font=("Helvetica", 14, "bold"), bg="pale goldenrod")
        self.email_label.grid(row=1, column=1, padx=10, pady=10)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=2, padx=10, pady=10)

        self.password_label = tk.Label(self, text="Password", font=("Helvetica", 14, "bold"), bg="pale goldenrod")
        self.password_label.grid(row=2, column=1, padx=10, pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=2, padx=10, pady=10)

        self.confirm_password_label = tk.Label(self, text="Confirm Password", font=("Helvetica", 14, "bold"), bg="pale goldenrod")
        self.confirm_password_label.grid(row=3, column=1, padx=10, pady=10)
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.grid(row=3, column=2, padx=10, pady=10)

        self.signup_button = tk.Button(self, text="Signup", command=self.signup, font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.signup_button.grid(row=4, column=1, pady=10)


    def signup(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not email or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if not check_email_unique(email):
            messagebox.showerror("Error", "Email already exists")
            return

        try:
            insert_user(username, email, password)
            messagebox.showinfo("Success", "Signup successful")
            self.controller.show_frame("LoginPage")
        except Exception as e:
            messagebox.showerror("Error", str(e))
