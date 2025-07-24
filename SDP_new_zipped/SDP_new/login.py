import tkinter as tk
from tkinter import messagebox
from database import get_user
from PIL import Image, ImageTk

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Set up the canvas for the background image
        self.canvas = tk.Canvas(self, width=self.controller.winfo_screenwidth(), height=self.controller.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        
        self.add_background()

        # Create a frame for the login form
        self.login_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window(0.5 * self.canvas.winfo_screenwidth(), 0.5 * self.canvas.winfo_screenheight(), window=self.login_frame, anchor="center")

        tk.Label(self.login_frame, text="WELCOME TO TIP TOP LAUNDRY SERVICE", bg="white", font=("Helvetica", 16, "bold")).grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        tk.Label(self.login_frame, text="Login", bg="white", font=("Helvetica", 16, "bold")).grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.username_label = tk.Label(self.login_frame, text="Username", bg="white",font=("Helvetica", 12, "bold"))
        self.username_label.grid(row=2, column=0, padx=10, pady=10)
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(self.login_frame, textvariable=self.username_var)
        self.username_entry.grid(row=2, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self.login_frame, text="Password", bg="white",font=("Helvetica", 12, "bold"))
        self.password_label.grid(row=3, column=0, padx=10, pady=10)
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.login_frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=3, column=1, padx=10, pady=10)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login,font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.login_button.grid(row=4, column=1, pady=10)

        self.signup_button = tk.Button(self.login_frame, text="Signup", command=lambda: self.controller.show_frame("SignupPage"),font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.signup_button.grid(row=4, column=0, pady=10)

    def add_background(self):
        try:
            # Load the background image
            img = Image.open("lan1.png")
            screen_width = self.controller.winfo_screenwidth()
            screen_height = self.controller.winfo_screenheight()
            img = img.resize((screen_width, screen_height), Image.BICUBIC)

            # Convert image to PhotoImage
            self.background_img = ImageTk.PhotoImage(img)

            # Add the image to the canvas
            self.canvas.create_image(0, 0, image=self.background_img, anchor="nw")
        except Exception as e:
            print("Error:", e)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin":  # Admin credentials
            self.controller.show_frame("AdminPage")
        else:
            user = get_user(username, password)
            if user:
                self.controller.show_frame("CustomerPage")
                self.controller.frames["InfoPage"].clear_clothes()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        self.clear_inputs()

    def clear_inputs(self):
        self.username_var.set("")
        self.password_var.set("")
