import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

from Entities.Transaction import Transaction
from Service.services import Service


# Import Service and Transaction classes


class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Manager")
        self.geometry("900x600")
        self.configure(bg="#2E4053")

        # Fonts and Colors
        self.primary_color = "#4A69BD"
        self.accent_color = "#6A89CC"
        self.text_color = "#F8C291"

        # Initialize the service layer
        self.service = Service()

        # Setup UI Elements
        self.create_header()
        self.create_dashboard()
        self.create_transaction_manager()

    def create_header(self):
        header = tk.Frame(self, bg=self.primary_color, height=50)
        header.pack(fill="x")

        title = tk.Label(header, text="Personal Finance Manager", font=("Helvetica", 18, "bold"), fg=self.text_color,
                         bg=self.primary_color)
        title.pack(pady=10)

    def create_dashboard(self):
        dashboard_frame = tk.Frame(self, bg=self.accent_color)
        dashboard_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Overview Section
        overview_frame = tk.Frame(dashboard_frame, bg=self.primary_color)
        overview_frame.pack(fill="x", pady=10)
        tk.Label(overview_frame, text="Dashboard Overview", font=("Helvetica", 14, "bold"), bg=self.primary_color,
                 fg=self.text_color).pack(pady=5)

        self.create_summary_boxes(overview_frame)
        self.create_graph_section(dashboard_frame)

    def create_summary_boxes(self, parent):
        summary_frame = tk.Frame(parent, bg=self.primary_color)
        summary_frame.pack(fill="x", padx=20, pady=10)

        categories = [("Income", "#1abc9c"), ("Expenses", "#e74c3c"), ("Available", "#3498db")]
        for category, color in categories:
            frame = tk.Frame(summary_frame, bg=color, width=150, height=100)
            frame.pack(side="left", padx=10, pady=10)
            tk.Label(frame, text=category, font=("Helvetica", 12, "bold"), bg=color, fg="white").pack(pady=10)
            tk.Label(frame, text=f"${random.randint(500, 2000)}", font=("Helvetica", 16), bg=color, fg="white").pack(
                pady=10)

    def create_graph_section(self, parent):
        graph_frame = tk.Frame(parent, bg=self.accent_color)
        graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Sample Pie Chart
        fig, ax = plt.subplots(figsize=(3, 3), dpi=80)
        labels = ['Food', 'Transport', 'Bills', 'Entertainment']
        sizes = [20, 30, 25, 25]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
               colors=['#2980b9', '#e74c3c', '#f1c40f', '#2ecc71'])
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, graph_frame)
        canvas.get_tk_widget().pack()

    def create_transaction_manager(self):
        transaction_frame = tk.Frame(self, bg="#34495e")
        transaction_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(transaction_frame, text="Transaction Manager", font=("Helvetica", 14, "bold"), bg="#34495e",
                 fg=self.text_color).pack(pady=5)

        # Listbox for Transactions
        self.transaction_listbox = tk.Listbox(transaction_frame, font=("Helvetica", 12), bg="#2E4053", fg="white",
                                              selectbackground=self.primary_color, height=10)
        self.transaction_listbox.pack(fill="both", expand=True, padx=20, pady=10)

        # Populate transactions
        self.populate_transactions()

        # Add transaction button
        add_button = tk.Button(transaction_frame, text="Add Transaction", command=self.add_transaction_form,
                               bg=self.primary_color, fg="white")
        add_button.pack(pady=10)

    def populate_transactions(self):
        # Clear the listbox
        self.transaction_listbox.delete(0, tk.END)

        # Fetch all transactions using Service
        transactions = self.service.get_all_transactions()
        for transaction in transactions:
            display_text = f"{transaction[1]} - ${transaction[2]} - {transaction[3]} - {transaction[5]}"
            self.transaction_listbox.insert(tk.END, display_text)

    def add_transaction_form(self):
        form_window = tk.Toplevel(self)
        form_window.title("Add Transaction")
        form_window.geometry("300x400")

        # Form fields
        tk.Label(form_window, text="Date (YYYY-MM-DD):").pack(pady=5)
        date_entry = tk.Entry(form_window)
        date_entry.pack()

        tk.Label(form_window, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(form_window)
        amount_entry.pack()

        tk.Label(form_window, text="Category:").pack(pady=5)
        category_entry = tk.Entry(form_window)
        category_entry.pack()

        tk.Label(form_window, text="Description:").pack(pady=5)
        description_entry = tk.Entry(form_window)
        description_entry.pack()

        tk.Label(form_window, text="Type (Income/Expense):").pack(pady=5)
        type_entry = tk.Entry(form_window)
        type_entry.pack()

        # Submit button
        submit_button = tk.Button(form_window, text="Submit", command=lambda: self.add_transaction(
            date_entry.get(), amount_entry.get(), category_entry.get(), description_entry.get(), type_entry.get(),
            form_window))
        submit_button.pack(pady=20)

    def add_transaction(self, date, amount, category, description, transaction_type, form_window):
        try:
            # Validate input fields
            if not date or not amount or not category or not transaction_type:
                messagebox.showerror("Error", "All fields are required.")
                return

            # Convert amount to float and validate
            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")
                return

            # Create Transaction instance and add it using Service
            transaction = Transaction(date=date, amount=amount, category=category, description=description,
                                      transaction_type=transaction_type)
            self.service.add_transaction(transaction)

            # Refresh the transaction list and close form
            self.populate_transactions()
            form_window.destroy()
            messagebox.showinfo("Success", "Transaction added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Run the app
app = FinanceApp()
app.mainloop()
