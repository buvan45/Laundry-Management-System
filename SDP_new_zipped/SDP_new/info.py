import tkinter as tk
from tkinter import ttk, messagebox
from database import insert_order  # Assume this is a function that inserts orders into your database
from datetime import datetime, timedelta
import random

class InfoPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_id = self.generateUniqueIDInt()   
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.clothes_table = None
        self.clothes = []
        self.create_widgets()

    def generateUniqueIDInt(self):
        return random.randint(1, 1000)

    def create_widgets(self):
        self.configure(bg="pale goldenrod")
        self.name_label = tk.Label(self, text="Name", font=("Helvetica", 14, "bold"))
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.phone_label = tk.Label(self, text="Phone", font=("Helvetica", 14, "bold"))
        self.phone_label.grid(row=1, column=0, padx=10, pady=10)
        self.phone_entry = tk.Entry(self, textvariable=self.phone_var)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)

        self.email_label = tk.Label(self, text="Email", font=("Helvetica", 14, "bold"))
        self.email_label.grid(row=2, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self, textvariable=self.email_var)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)

        self.confirm_button = tk.Button(self, text="Confirm", command=self.confirm_order, font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.confirm_button.grid(row=3, column=1, pady=10)

        self.back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("CustomerPage"), font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.back_button.grid(row=4, column=0, pady=10)

        self.signout_button = tk.Button(self, text="Signout", command=lambda: self.controller.show_frame("LoginPage"), font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.signout_button.grid(row=4, column=1, pady=10)

        self.create_order_table()

    def create_order_table(self):
        self.clothes_table = ttk.Treeview(self, columns=("Cloth", "Laundry", "Total Price", "User ID", "Delivery Date"), show="headings")
        self.clothes_table.heading("Cloth", text="Cloth")
        self.clothes_table.heading("Laundry", text="Laundry")
        self.clothes_table.heading("Total Price", text="Total Price")
        self.clothes_table.heading("User ID", text="User ID")
        self.clothes_table.heading("Delivery Date", text="Delivery Date")
        self.clothes_table.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def add_cloth(self, cloth, laundry, cost):
        self.clothes.append((cloth, laundry, cost))
        self.update_order_table()

    def update_order_table(self):
        self.clear_order_table()
        total_price = 0
        num_clothes = len(self.clothes)
        delivery_date = self.calculate_delivery_date(num_clothes)
        for cloth, laundry, price in self.clothes:
            total_price += price
            self.clothes_table.insert("", "end", values=(cloth, laundry, price, self.user_id, delivery_date))
        self.clothes_table.insert("", "end", values=("Total", "", total_price, "", ""))

    def clear_order_table(self):
        for item in self.clothes_table.get_children():
            self.clothes_table.delete(item)
    
    def clear_clothes(self):
        self.clothes = []  # Clear cloth information
        self.update_order_table()

    def calculate_delivery_date(self, num_clothes):
        if num_clothes == 1:
            return (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        elif 2 <= num_clothes <= 5:
            return (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        else:
            return (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')

    def confirm_order(self):
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        if name and phone and email:
            total_price = sum(price for _, _, price in self.clothes)
            self.controller.frames["AdminPage"].display_order_information(self.user_id, name, phone, email, self.clothes, total_price)
            
            num_clothes = len(self.clothes)
            delivery_date = self.calculate_delivery_date(num_clothes)

            for cloth, laundry, cost in self.clothes:
                insert_order(self.user_id, name, cloth, laundry, cost, delivery_date, "Pending")
            messagebox.showinfo("Success", "Order Confirmed")
 
            self.clear_inputs()
            self.clear_clothes()
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def clear_inputs(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
