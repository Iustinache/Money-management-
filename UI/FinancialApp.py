import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from Database.database import Repository  # Assuming Repository is your database handling class
from Entities.Transaction import Transaction  # Assuming your Transaction class is in Entities module
from Service.services import Service


class FinancialApp:
    def __init__(self, root, service):
        self.root = root
        self.service = service
        self.root.title("Financial Management System")
        self.root.geometry("600x400")
        self.root.config(bg="#f7f7f7")

        # Define frame for layout
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title_label = ttk.Label(self.frame, text="Financial Management", font=("Helvetica", 20, "bold"),
                                     anchor="center")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Date Entry
        self.date_label = ttk.Label(self.frame, text="Date (YYYY-MM-DD)", font=("Helvetica", 12))
        self.date_label.grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.frame, width=30)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        # Amount Entry
        self.amount_label = ttk.Label(self.frame, text="Amount", font=("Helvetica", 12))
        self.amount_label.grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.frame, width=30)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        # Category Entry
        self.category_label = ttk.Label(self.frame, text="Category", font=("Helvetica", 12))
        self.category_label.grid(row=3, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.frame, width=30)
        self.category_entry.grid(row=3, column=1, padx=5, pady=5)

        # Description Entry
        self.description_label = ttk.Label(self.frame, text="Description", font=("Helvetica", 12))
        self.description_label.grid(row=4, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.frame, width=30)
        self.description_entry.grid(row=4, column=1, padx=5, pady=5)

        # Transaction Type
        self.transaction_type_label = ttk.Label(self.frame, text="Transaction Type (income/expense)",
                                                font=("Helvetica", 12))
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
        # Clear the current listbox items
        self.transaction_listbox.delete(0, tk.END)

        # Load transactions from the repository
        transactions = self.service.get_all_transactions()
        for t in transactions:
            self.transaction_listbox.insert(tk.END,
                                            f"{t[1]} - {t[2]} {t[3]} - {t[5]}")  # format as "Date - Amount Category Type"

    def add_transaction(self):
        try:
            date = self.date_entry.get()
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()
            transaction_type = self.transaction_type_entry.get()

            # Create the Transaction object
            transaction = Transaction(None, date, amount, category, description, transaction_type)
            self.service.add_transaction(transaction)
            self.load_transactions()
            messagebox.showinfo("Success", "Transaction added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_transaction(self):
        try:
            selected_transaction = self.transaction_listbox.curselection()
            if not selected_transaction:
                raise ValueError("Please select a transaction to update.")

            # Get the transaction ID
            selected_index = selected_transaction[0]
            transaction_data = self.service.get_all_transactions()[selected_index]
            transaction_id = transaction_data[0]

            # Get new values
            new_date = simpledialog.askstring("Update Date", "Enter new date (YYYY-MM-DD):")
            new_amount = simpledialog.askfloat("Update Amount", "Enter new amount:")
            new_category = simpledialog.askstring("Update Category", "Enter new category:")
            new_description = simpledialog.askstring("Update Description", "Enter new description:")
            new_type = simpledialog.askstring("Update Type", "Enter new transaction type (income/expense):")

            updated_transaction = Transaction(transaction_id, new_date, new_amount, new_category, new_description,
                                              new_type)
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

            # Get the transaction ID
            selected_index = selected_transaction[0]
            transaction_data = self.service.get_all_transactions()[selected_index]
            transaction_id = transaction_data[0]

            self.service.delete_transaction(transaction_id)
            self.load_transactions()
            messagebox.showinfo("Success", "Transaction deleted successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))


# Create the Tkinter window
root = tk.Tk()

# Assuming you have a `Service` class initialized with your Repository
service = Service(Repository())

# Create the GUI application
app = FinancialApp(root, service)

# Run the application
root.mainloop()
