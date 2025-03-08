import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Entities.Transaction import Transaction
from Service.services import Service


class FinancialApp:
    def __init__(self, root, service, user_id, open_login_callback):
        self.root = root
        self.service = service
        self.user_id = user_id
        self.open_login_callback = open_login_callback
        self.root.title("Financial Management System")
        self.root.geometry("800x600")  # Mărește dimensiunea ferestrei
        self.root.config(bg="#f7f7f7")

        # Crează un canvas și un scrollbar
        self.canvas = tk.Canvas(self.root, bg="#f7f7f7")
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configurează canvas-ul
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Adaugă scrollable_frame la canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configurează scrollbar-ul
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Plasează canvas și scrollbar în fereastră
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Folosește scrollable_frame în loc de self.frame
        self.frame = self.scrollable_frame

        self.style = ttk.Style()
        self.style.configure("Highlight.TFrame", background="lightgreen")

        self.create_widgets()
        self.create_transactions_table()
        self.create_buttons_panel()
        self.create_financial_summary_panel()
        # self.create_monthly_summary_panel()
        self.create_charts_panel()
        self.refresh_dashboard()

        # Butonul Exit
        self.exit_button = ttk.Button(self.frame, text="Exit", command=self.exit_to_login)
        self.exit_button.grid(row=7, column=0, columnspan=2, pady=10)

    def exit_to_login(self):
        """Închide fereastra curentă și redeschide fereastra de login."""
        self.root.destroy()  # Închide fereastra FinancialApp
        self.open_login_callback()  # Reafișează LoginScreen

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

        # Butonul Exit (păstrat în partea de sus)
        self.exit_button = ttk.Button(self.frame, text="Exit", command=self.exit_to_login)
        self.exit_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Ajustarea dimensiunilor coloanelor și rândurilor
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(7, weight=1)

    def create_transactions_table(self):
        """Creează un tabel pentru afișarea tranzacțiilor."""
        self.transactions_frame = ttk.Frame(self.frame, padding="10")
        self.transactions_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky="nsew")

        # Titlu pentru tabelul de tranzacții
        ttk.Label(self.transactions_frame, text="Transactions", font=("Helvetica", 14, "bold")).grid(row=0, column=0,
                                                                                                     columnspan=5,
                                                                                                     pady=5)

        # Crearea tabelului
        self.transactions_table = ttk.Treeview(
            self.transactions_frame,
            columns=("ID", "Date", "Amount", "Category", "Description", "Type"),
            show="headings"
        )
        self.transactions_table.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

        # Adăugarea coloanelor
        self.transactions_table.heading("ID", text="ID")
        self.transactions_table.heading("Date", text="Date")
        self.transactions_table.heading("Amount", text="Amount")
        self.transactions_table.heading("Category", text="Category")
        self.transactions_table.heading("Description", text="Description")
        self.transactions_table.heading("Type", text="Type")

        # Ajustarea dimensiunilor coloanelor
        self.transactions_table.column("ID", width=50, anchor="center")
        self.transactions_table.column("Date", width=100, anchor="center")
        self.transactions_table.column("Amount", width=100, anchor="center")
        self.transactions_table.column("Category", width=150, anchor="center")
        self.transactions_table.column("Description", width=200, anchor="center")
        self.transactions_table.column("Type", width=100, anchor="center")

        # Adăugarea unui scrollbar
        scrollbar = ttk.Scrollbar(self.transactions_frame, orient="vertical", command=self.transactions_table.yview)
        scrollbar.grid(row=1, column=5, sticky="ns")
        self.transactions_table.configure(yscrollcommand=scrollbar.set)

        # Ajustarea dimensiunilor cadrului
        self.transactions_frame.grid_columnconfigure(0, weight=1)
        self.transactions_frame.grid_rowconfigure(1, weight=1)

    def create_buttons_panel(self):
        """Creează un panou pentru butoanele de adăugare/actualizare/ștergere."""
        self.buttons_frame = ttk.Frame(self.frame, padding="10")
        self.buttons_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

        # Butoane
        self.add_button = ttk.Button(self.buttons_frame, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.update_button = ttk.Button(self.buttons_frame, text="Update Transaction", command=self.update_transaction)
        self.update_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.delete_button = ttk.Button(self.buttons_frame, text="Delete Transaction", command=self.delete_transaction)
        self.delete_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Ajustarea dimensiunilor coloanelor
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)
        self.buttons_frame.grid_columnconfigure(2, weight=1)


    def load_transactions(self):
        """Încarcă tranzacțiile în tabel."""
        # Șterge toate rândurile existente
        for row in self.transactions_table.get_children():
            self.transactions_table.delete(row)

        # Obține tranzacțiile din serviciu
        transactions = self.service.get_all_transactions_by_user(self.user_id)

        # Adaugă tranzacțiile în tabel
        for t in transactions:
            self.transactions_table.insert("", "end", values=t)

    def create_financial_summary_panel(self):
        self.summary_frame = ttk.Frame(self.frame, padding="10", style="TFrame")
        self.summary_frame.grid(row=10, column=0, columnspan=2, pady=10, sticky="ew")

        # Titlu pentru panoul de sumar financiar
        ttk.Label(self.summary_frame, text="Financial Summary", font=("Helvetica", 14, "bold")).grid(row=0, column=0,
                                                                                                     columnspan=2,
                                                                                                     pady=5)

        # Etichete și valori
        ttk.Label(self.summary_frame, text="Total Income:", anchor="center").grid(row=1, column=0, padx=5, pady=5,
                                                                                  sticky="ew")
        ttk.Label(self.summary_frame, text="0", anchor="center").grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.summary_frame, text="Total Expenses:", anchor="center").grid(row=2, column=0, padx=5, pady=5,
                                                                                    sticky="ew")
        ttk.Label(self.summary_frame, text="0", anchor="center").grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.summary_frame, text="Available Budget:", anchor="center").grid(row=3, column=0, padx=5, pady=5,
                                                                                      sticky="ew")
        ttk.Label(self.summary_frame, text="0", anchor="center").grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Ajustarea dimensiunilor coloanelor
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=1)

    def create_charts_panel(self):
        self.charts_frame = ttk.Frame(self.frame, padding="10", style="TFrame", relief="solid", borderwidth=1)
        self.charts_frame.grid(row=12, column=0, columnspan=2, pady=10, sticky="ew")

        # Titlu pentru panoul de grafice
        ttk.Label(self.charts_frame, text="Charts and Statistics", font=("Helvetica", 14, "bold")).grid(row=0, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=5)

        # Graficul pentru distribuția cheltuielilor pe categorii
        categories = self.service.get_category_spending(self.user_id)
        fig1, ax1 = plt.subplots()
        ax1.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        ax1.set_title("Expense Distribution by Category")
        canvas1 = FigureCanvasTkAgg(fig1, master=self.charts_frame)
        canvas1.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)

        # Graficul pentru evoluția veniturilor și cheltuielilor în timp
        trend = self.service.get_income_expense_trend(self.user_id)
        dates = sorted(trend.keys())
        income = [trend[date]["income"] for date in dates]
        expenses = [trend[date]["expense"] for date in dates]
        fig2, ax2 = plt.subplots()
        ax2.plot(dates, income, label="Income")
        ax2.plot(dates, expenses, label="Expenses")
        ax2.set_title("Income and Expenses Over Time")
        ax2.legend()
        canvas2 = FigureCanvasTkAgg(fig2, master=self.charts_frame)
        canvas2.get_tk_widget().grid(row=0, column=1, padx=5, pady=5)

        # Ajustarea dimensiunilor coloanelor
        self.charts_frame.grid_columnconfigure(0, weight=1)
        self.charts_frame.grid_columnconfigure(1, weight=1)

    def add_transaction(self):
        try:
            date = self.date_entry.get()
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()
            transaction_type = self.transaction_type_entry.get().strip().lower()

            if transaction_type not in ["income", "expense"]:
                raise ValueError("Transaction type must be 'income' or 'expense'.")

            transaction = Transaction(None, date, amount, category, description, transaction_type)
            self.service.add_transaction(self.user_id, transaction)
            self.refresh_dashboard()  # Actualizează dashboard-ul
            self.highlight_panels()
            messagebox.showinfo("Success", "Transaction added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_transaction(self):
        try:
            selected_transaction = self.transactions_table.selection()
            if not selected_transaction:
                raise ValueError("Please select a transaction to update.")

            transaction_id = self.transactions_table.item(selected_transaction, "values")[0]

            # Ask the user for new values
            new_date = simpledialog.askstring("Update Date", "Enter new date (YYYY-MM-DD):")
            new_amount = simpledialog.askfloat("Update Amount", "Enter new amount:")
            new_category = simpledialog.askstring("Update Category", "Enter new category:")
            new_description = simpledialog.askstring("Update Description", "Enter new description:")
            new_type = simpledialog.askstring("Update Type", "Enter new transaction type (income/expense):")

            if new_type not in ["income", "expense"]:
                raise ValueError("Transaction type must be 'income' or 'expense'.")

            updated_transaction = Transaction(transaction_id, new_date, new_amount, new_category, new_description,
                                              new_type)
            self.service.update_transaction(transaction_id, updated_transaction)
            self.refresh_dashboard()  # Actualizează dashboard-ul
            self.highlight_panels()
            messagebox.showinfo("Success", "Transaction updated successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_transaction(self):
        try:
            selected_transaction = self.transactions_table.selection()
            if not selected_transaction:
                raise ValueError("Please select a transaction to delete.")

            transaction_id = self.transactions_table.item(selected_transaction, "values")[0]

            self.service.delete_transaction(transaction_id)
            self.refresh_dashboard()  # Actualizează dashboard-ul
            self.highlight_panels()
            messagebox.showinfo("Success", "Transaction deleted successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def exit_application(self):
        exit(0)

    def refresh_dashboard(self):
        """Reîmprospătează dashboard-ul și adaugă un efect de highlight."""
        self.load_transactions()
        self.update_financial_summary()
        self.root.after(100, self.update_charts)  # Amână actualizarea graficelor
        self.highlight_panels()

    def update_financial_summary(self):
        """Actualizează doar conținutul panoului de sumar financiar."""
        if self.summary_frame:
            financial_summary = self.service.get_financial_summary(self.user_id)
            for i, (label, value) in enumerate(zip(
                    ["Total Venituri:", "Total Cheltuieli:", "Buget Disponibil:"],
                    [financial_summary["total_income"], financial_summary["total_expenses"],
                     financial_summary["available_budget"]]
            )):
                self.summary_frame.grid_slaves(row=i, column=1)[0].config(text=f"{value}")

    def update_charts(self):
        """Actualizează doar graficele."""
        if self.charts_frame:
            for widget in self.charts_frame.winfo_children():
                widget.destroy()
            self.create_charts_panel()

    def highlight_panels(self):
        """Adaugă un efect de highlight pe panouri."""
        for frame in [self.summary_frame, self.charts_frame]:
            if frame:
                frame.configure(style="Highlight.TFrame")  # Aplică stilul de highlight
                self.root.after(500,
                                lambda f=frame: f.configure(style="TFrame"))  # Revine la stilul implicit după 500ms
