import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from Entities.Transaction import Transaction
from Service.services import Service

class FinancialApp:
    def __init__(self, root, service, user_id):
        self.root = root
        self.service = service
        self.user_id = user_id  # To track the user ID for transactions
        self.root.title("Financial Management System")
        self.root.geometry("600x400")
        self.root.config(bg="#f7f7f7")

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self.frame, text="Financial Management", font=("Helvetica", 20, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Date Entry
        self.date_label = ttk.Label(self.frame, text="Date (YYYY-MM-DD)")
        self.date_label.grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.frame, width=30)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        # Amount Entry
        self.amount_label = ttk.Label(self.frame, text="Amount")
        self.amount_label.grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.frame, width=30)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        # Category Entry
        self.category_label = ttk.Label(self.frame, text="Category")
        self.category_label.grid(row=3, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.frame, width=30)
        self.category_entry.grid(row=3, column=1, padx=5, pady=5)

        # Description Entry
        self.description_label = ttk.Label(self.frame, text="Description")
        self.description_label.grid(row=4, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.frame, width=30)
        self.description_entry.grid(row=4, column=1, padx=5, pady=5)

        # Transaction Type
        self.transaction_type_label = ttk.Label(self.frame, text="Transaction Type (income/expense)")
        self.transaction_type_label.grid(row=5, column=0, padx=5, pady=5)
        self.transaction_type_entry = ttk.Entry(self.frame, width=30)
        self.transaction_type_entry.grid(row=5, column=1, padx=5, pady=5)

        # Buttons
        self.add_button = ttk.Button(self.frame, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=6, column=0, padx=5, pady=10, sticky="ew")

        self.update_button = ttk.Button(self.frame, text="Update Transaction", command=self.update_transaction)
        self.update_button.grid(row=6, column=1, padx=5, pady=10, sticky="ew")

        self.delete_button = ttk.Button(self.frame, text="Delete Transaction", command=self.delete_transaction)
        self.delete_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Transaction Listbox
        self.transaction_listbox = tk.Listbox(self.frame, height=6, width=50, font=("Helvetica", 12))
        self.transaction_listbox.grid(row=8, column=0, columnspan=2, padx=5, pady=10)
        self.load_transactions()

    def load_transactions(self):
        self.transaction_listbox.delete(0, tk.END)

        transactions = self.service.get_all_transactions_by_user(self.user_id)  # Filter by user_id
        for t in transactions:
            self.transaction_listbox.insert(tk.END, f"{t[1]} - {t[2]} {t[3]} - {t[5]}")

    def add_transaction(self):
        try:
            date = self.date_entry.get()
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()
            transaction_type = self.transaction_type_entry.get().strip().lower()

            if transaction_type not in ["income", "expense"]:
                raise ValueError("Transaction type must be 'income' or 'expense'.")

            # Ensure transaction_type is passed correctly
            print(f"Transaction type: {transaction_type}")  # Debugging print statement

            transaction = Transaction(None, date, amount, category, description, transaction_type)
            self.service.add_transaction(self.user_id, transaction)  # Pass the user_id to the service
            self.load_transactions()
            messagebox.showinfo("Success", "Transaction added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_transaction(self):
        try:
            selected_transaction = self.transaction_listbox.curselection()
            if not selected_transaction:
                raise ValueError("Please select a transaction to update.")

            selected_index = selected_transaction[0]
            transaction_data = self.service.get_all_transactions_by_user(self.user_id)[selected_index]
            transaction_id = transaction_data[0]

            # Ask the user for new values
            new_date = simpledialog.askstring("Update Date", "Enter new date (YYYY-MM-DD):")
            new_amount = simpledialog.askfloat("Update Amount", "Enter new amount:")
            new_category = simpledialog.askstring("Update Category", "Enter new category:")
            new_description = simpledialog.askstring("Update Description", "Enter new description:")
            new_type = simpledialog.askstring("Update Type", "Enter new transaction type (income/expense):")

            if new_type not in ["income", "expense"]:
                raise ValueError("Transaction type must be 'income' or 'expense'.")

            # Ensure transaction_type is passed correctly when updating
            updated_transaction = Transaction(transaction_id, new_date, new_amount, new_category, new_description, new_type)
            self.service.update_transaction(transaction_id, updated_transaction)
            self.load_transactions()
            messagebox.showinfo("Success", "Transaction updated successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_transaction(self):
        try:
            selected_transaction = self.transaction_listbox.curselection()
            if not selected_transaction:
                raise ValueError("Please select a transaction to delete.")

            selected_index = selected_transaction[0]
            transaction_data = self.service.get_all_transactions_by_user(self.user_id)[selected_index]
            transaction_id = transaction_data[0]

            self.service.delete_transaction(transaction_id)
            self.load_transactions()
            messagebox.showinfo("Success", "Transaction deleted successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
