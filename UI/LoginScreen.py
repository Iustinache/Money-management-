import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from FinancialApp import FinancialApp
from Database.database import Database  # Modul pentru gestionarea bazei de date
from Service.services import Service
import bcrypt

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")
        self.root.config(bg="#f7f7f7")

        self.db = Database()  # Instanța bazei de date

        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(expand=True)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Username", font=("Helvetica", 12)).pack(pady=5)
        self.username_entry = ttk.Entry(self.frame, width=30)
        self.username_entry.pack(pady=5)

        ttk.Label(self.frame, text="Password", font=("Helvetica", 12)).pack(pady=5)
        self.password_entry = ttk.Entry(self.frame, width=30, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self.frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.signup_button = ttk.Button(self.frame, text="Create New Account", command=self.create_account)
        self.signup_button.pack(pady=10)

        self.exit_button = ttk.Button(self.frame, text="Exit", command=self.exit_application)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user_id = self.authenticate(username, password)
        if user_id:
            messagebox.showinfo("Success", "Login successful!")
            self.root.withdraw()  # Ascunde fereastra de login
            open_financial_app(user_id, self.show)  # Deschide FinancialApp cu callback
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show(self):
        """Afișează fereastra de login."""
        self.root.deiconify()  # Reafișează fereastra de login

    def authenticate(self, username, password):
        """Verifică dacă username-ul și parola sunt corecte și returnează user_id."""
        user = self.db.fetch_one("SELECT id, password FROM users WHERE username = ?", (username,))
        if user:
            user_id, stored_password = user
            if bcrypt.checkpw(password.encode("utf-8"), stored_password):
                return user_id  # Returnează user_id
        return None

    def create_account(self):
        def submit_account():
            username = new_username_entry.get()
            password = new_password_entry.get()

            if username and password:
                if self.username_exists(username):
                    messagebox.showerror("Error", "Username already exists")
                else:
                    self.create_new_user(username, password)
                    messagebox.showinfo("Success", "Account created successfully!")
                    new_account_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter both username and password")

        # Fereastră nouă pentru crearea unui cont
        new_account_window = tk.Toplevel(self.root)
        new_account_window.title("Create New Account")
        new_account_window.geometry("400x300")

        ttk.Label(new_account_window, text="New Username", font=("Helvetica", 12)).pack(pady=5)
        new_username_entry = ttk.Entry(new_account_window, width=30)
        new_username_entry.pack(pady=5)

        ttk.Label(new_account_window, text="New Password", font=("Helvetica", 12)).pack(pady=5)
        new_password_entry = ttk.Entry(new_account_window, width=30, show="*")
        new_password_entry.pack(pady=5)

        submit_button = ttk.Button(new_account_window, text="Create Account", command=submit_account)
        submit_button.pack(pady=20)

    def username_exists(self, username):
        """Verifică dacă username-ul există deja în baza de date."""
        user = self.db.fetch_one("SELECT * FROM users WHERE username = ?", (username,))
        return user is not None

    def create_new_user(self, username, password):
        """Creează un utilizator nou cu parolă hashuită."""
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.db.execute_query("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))

    def exit_application(self):
        exit(0)


def open_financial_app(user_id, open_login_callback):
    root = tk.Tk()
    service = Service(Database())
    FinancialApp(root, service, user_id, open_login_callback)
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
