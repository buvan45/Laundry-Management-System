import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from database import insert_order, get_user

class CustomerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_id = None
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="pale goldenrod")

        self.widgets_frame = tk.Frame(self, bg="pale goldenrod")  # Frame to hold widgets with background color
        self.widgets_frame.pack(padx=10, pady=10)

        self.type_label = tk.Label(self.widgets_frame, text="Type of Cloth", font=("Helvetica", 14, "bold"))
        self.type_label.grid(row=0, column=0, padx=10, pady=10)

        self.type_var = tk.StringVar()
        self.type_combobox = ttk.Combobox(self.widgets_frame, textvariable=self.type_var)
        self.type_combobox['values'] = ("Cotton", "Silk", "Woolen", "Others")
        self.type_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.laundry_label = tk.Label(self.widgets_frame, text="Type of Laundry", font=("Helvetica", 14, "bold"))
        self.laundry_label.grid(row=1, column=0, padx=10, pady=10)

        self.laundry_var = tk.StringVar()
        self.laundry_combobox = ttk.Combobox(self.widgets_frame, textvariable=self.laundry_var)
        self.laundry_combobox['values'] = ("Cotton Care", "Silk Care", "Dry Clean", "Dry Wash", "Others")
        self.laundry_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.widgets_frame, text="Add Cloth", command=self.add_cloth, font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.add_button.grid(row=2, column=1, pady=10)

        self.next_button = tk.Button(self.widgets_frame, text="Next", command=self.next_page, font=("Helvetica", 12, "bold"), fg="white", bg="blue", relief=tk.GROOVE)
        self.next_button.grid(row=3, column=1, pady=10)

    
    def add_cloth(self):
        cloth_type = self.type_var.get()
        laundry_type = self.laundry_var.get()
        if cloth_type and laundry_type:
            cost = self.calculate_cost(cloth_type, laundry_type)
            self.controller.frames["InfoPage"].add_cloth(cloth_type, laundry_type, cost)
            messagebox.showinfo("Success", f"Added {cloth_type} - {laundry_type} - {cost}")
        else:
            messagebox.showerror("Error", "Please select both cloth type and laundry type")

    def calculate_cost(self, cloth_type, laundry_type):
        prices = {
            "Cotton": 100,
            "Silk": 200,
            "Woolen": 250,
            "Others": 300,
            "Cotton Care": 150,
            "Silk Care": 250,
            "Dry Clean": 250,
            "Dry Wash": 300,
            "Others": 300,
        }
        return prices[cloth_type] + prices[laundry_type]

    def next_page(self):
        self.controller.show_frame("InfoPage")
