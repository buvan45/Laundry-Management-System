import tkinter as tk
from tkinter import ttk
from login import LoginPage
from signup import SignupPage
from customer import CustomerPage
from admin import AdminPage
from info import InfoPage
import database

class LaundryManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Laundry Management System")
        self.geometry("800x600")
        self.frames = {}
        self.create_frames()
        database.connect()

    def create_frames(self):
        for F in (LoginPage, SignupPage, CustomerPage, InfoPage, AdminPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = LaundryManagementSystem()
    app.mainloop()
