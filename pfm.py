import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

class FinanceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.root.geometry("1920x1080")
        
        # Set up the main frame
        self.frame = ttkb.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Labels and Entries for Income
        self.income_label = ttkb.Label(self.frame, text="Income")
        self.income_label.grid(row=0, column=0, pady=5)
        self.income_entry = ttkb.Entry(self.frame, width=25)
        self.income_entry.grid(row=0, column=1, pady=5)
        
        # Labels and Entries for Expense
        self.expense_label = ttkb.Label(self.frame, text="Expense")
        self.expense_label.grid(row=1, column=0, pady=5)
        self.expense_entry = ttkb.Entry(self.frame, width=25)
        self.expense_entry.grid(row=1, column=1, pady=5)
        
        # Labels and Entries for Expense Category
        self.category_label = ttkb.Label(self.frame, text="Category")
        self.category_label.grid(row=2, column=0, pady=5)
        self.category_entry = ttkb.Entry(self.frame, width=25)
        self.category_entry.grid(row=2, column=1, pady=5)
        
        # Add Buttons
        self.add_income_button = ttkb.Button(self.frame, text="Add Income", command=self.add_income, bootstyle=SUCCESS)
        self.add_income_button.grid(row=3, column=0, pady=5)
        self.add_expense_button = ttkb.Button(self.frame, text="Add Expense", command=self.add_expense, bootstyle=DANGER)
        self.add_expense_button.grid(row=3, column=1, pady=5)
        
        # Show Data Button
        self.show_data_button = ttkb.Button(self.frame, text="Show Data", command=self.show_data, bootstyle=INFO)
        self.show_data_button.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Canvas for Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2, pady=20)
        
        # Initialize data
        self.data = pd.DataFrame(columns=["Type", "Amount", "Category"])

    def add_income(self):
        amount = self.income_entry.get()
        if amount:
            try:
                amount = float(amount)
                new_row = pd.DataFrame([{"Type": "Income", "Amount": amount, "Category": "Income"}])
                self.data = pd.concat([self.data, new_row], ignore_index=True)
                self.income_entry.delete(0, tk.END)
                print(f"Added Income: {amount}")
                messagebox.showinfo("Success", "Income added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for income")
        else:
            messagebox.showwarning("Warning", "Please enter an amount")

    def add_expense(self):
        amount = self.expense_entry.get()
        category = self.category_entry.get()
        if amount and category:
            try:
                amount = float(amount)
                new_row = pd.DataFrame([{"Type": "Expense", "Amount": amount, "Category": category}])
                self.data = pd.concat([self.data, new_row], ignore_index=True)
                self.expense_entry.delete(0, tk.END)
                self.category_entry.delete(0, tk.END)
                print(f"Added Expense: {amount} in Category: {category}")
                messagebox.showinfo("Success", "Expense added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for expense")
        else:
            messagebox.showwarning("Warning", "Please enter an amount and category")

    def show_data(self):
        if not self.data.empty:
            self.ax.clear()
            income = self.data[self.data["Type"] == "Income"]["Amount"].sum()
            expenses = self.data[self.data["Type"] == "Expense"].groupby("Category")["Amount"].sum()
            
            # Pie chart for expenses
            self.ax.pie(expenses, labels=expenses.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("husl", len(expenses)))
            self.ax.set_title(f"Expenses Distribution (Total Income: {income})")
            
            self.canvas.draw()
            print("Data shown successfully")
        else:
            messagebox.showinfo("Info", "No data to display")

if __name__ == "__main__":
    root = ttkb.Window(themename="darkly")
    app = FinanceManager(root)
    root.mainloop()
