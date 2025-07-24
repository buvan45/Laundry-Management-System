import tkinter as tk
from tkinter import ttk, messagebox
from database import get_all_users, get_report, update_status  # Assuming you have an `update_transaction_status` function in your database module
import random

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.report_table = None
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="pale goldenrod")
        self.info_label = tk.Label(self, text="All Customer Information", font=("Helvetica", 14, "bold"))
        self.info_label.grid(row=0, column=0, padx=10, pady=10)

        self.load_button = tk.Button(self, text="Load Data", command=self.load_data, font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.load_button.grid(row=1, column=0, padx=10, pady=10)

        self.report_label = tk.Label(self, text="Reports (Daily/Weekly/Monthly)", font=("Helvetica", 14, "bold"))
        self.report_label.grid(row=2, column=0, padx=10, pady=10)

        self.report_combobox = ttk.Combobox(self)
        self.report_combobox['values'] = ("Daily", "Weekly", "Monthly")
        self.report_combobox.grid(row=2, column=1, padx=10, pady=10)

        self.generate_button = tk.Button(self, text="Generate Report", command=self.generate_report, font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.generate_button.grid(row=3, column=1, pady=10)

        self.update_status_button = tk.Button(self, text="Update Status", command=self.update_status, font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.update_status_button.grid(row=4, column=0, pady=10)

        self.signout_button = tk.Button(self, text="Signout", command=lambda: self.controller.show_frame("LoginPage"), font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.signout_button.grid(row=5, column=0, pady=10)

    def display_order_information(self, user_id, name, phone, email, clothes, total_price):
        if self.report_table:
            self.report_table.destroy()

        self.report_table = ttk.Treeview(self, columns=("User ID", "Name", "Phone", "Email", "Cloth", "Laundry", "Total Price"), show="headings")
        self.report_table.heading("User ID", text="User ID")
        self.report_table.heading("Name", text="Name")
        self.report_table.heading("Phone", text="Phone")
        self.report_table.heading("Email", text="Email")
        self.report_table.heading("Cloth", text="Cloth")
        self.report_table.heading("Laundry", text="Laundry")
        self.report_table.heading("Total Price", text="Total Price")

        self.report_table.insert("", "end", values=(user_id, name, phone, email, "", "", ""))  # Insert user info row

        for cloth, laundry, price in clothes:
            self.report_table.insert("", "end", values=("", "", "", "", cloth, laundry, price))

        self.report_table.insert("", "end", values=("", "", "", "", "Total", "", total_price))  # Insert total row

        self.report_table.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def load_data(self):
        users = get_all_users()

        data_window = tk.Toplevel(self)
        data_window.title("Customer Information")

        data_table = ttk.Treeview(data_window, columns=("Unique ID", "Username", "Email"), show="headings")
        data_table.heading("Unique ID", text="Unique ID")
        data_table.heading("Username", text="Username")
        data_table.heading("Email", text="Email")

        unique_ids = set()
        for user in users:
            while True:
                unique_id = random.randint(1, 1000)
                if unique_id not in unique_ids:
                    unique_ids.add(unique_id)
                    break
            data_table.insert("", "end", values=(unique_id, user[1], user[2]))  # Assuming user[1] is username and user[2] is email

        data_table.pack(fill="both", expand=True)

    def generate_report(self):
        period = self.report_combobox.get().lower()
        if period:
            report = get_report()
            self.display_report_table(report)
        else:
            messagebox.showerror("Error", "Please select a report period")

    def display_report_table(self, report):
        if self.report_table:
            self.report_table.destroy()

        self.report_table = ttk.Treeview(self, columns=("Name", "Email", "Cloth", "Laundry", "Total Price", "Delivery Date", "Status"), show="headings")
        self.report_table.heading("Name", text="Name")
        self.report_table.heading("Email", text="Email")
        self.report_table.heading("Cloth", text="Cloth")
        self.report_table.heading("Laundry", text="Laundry")
        self.report_table.heading("Total Price", text="Total Price")
        self.report_table.heading("Delivery Date", text="Delivery Date")
        self.report_table.heading("Status", text="Status")

        total_revenue = 0

        for entry in report:
            name, email, cloth, laundry, cost, delivery_date, status = entry
            self.report_table.insert("", "end", values=(name, email, cloth, laundry, cost, delivery_date, status))
            total_revenue += cost

        self.report_table.insert("", "end", values=("Total Revenue", "", "", "", total_revenue, ""))

        self.report_table.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def update_status(self):
        selected_item = self.report_table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No transaction selected")
            return

        item_values = self.report_table.item(selected_item)["values"]
        if item_values:
            name, email, cloth, laundry, cost, status = item_values[0], item_values[1], item_values[2], item_values[3], item_values[4], item_values[5]
            update_status(name, cloth, laundry, cost, "Paid")
            messagebox.showinfo("Success", "Status updated successfully")
            self.generate_report()
