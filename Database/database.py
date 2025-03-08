import sqlite3

class Database:
    def __init__(self, db_name="finance.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def execute_query(self, query, params=()):
        """Execută o interogare care modifică baza de date (INSERT, UPDATE, DELETE)."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def fetch_one(self, query, params=()):
        """Execută o interogare și returnează un singur rezultat."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result

    def fetch_all(self, query, params=()):
        """Execută o interogare și returnează toate rezultatele."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result

    def create_tables(self):
        """Creează tabelele necesare (users și transactions)."""
        query_users = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL
        )
        """
        self.execute_query(query_users)

        query_transactions = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT,
            amount REAL,
            category TEXT,
            description TEXT,
            transaction_type TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        self.execute_query(query_transactions)

    # Adăugare tranzacție
    def add_transaction(self, user_id, transaction):
        query = """
        INSERT INTO transactions (user_id, date, amount, category, description, transaction_type)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.execute_query(query, (user_id, transaction.get_date(), transaction.get_amount(),
                                   transaction.get_category(), transaction.get_description(),
                                   transaction.get_transaction_type()))

    # Obținere tranzacții după user_id
    def get_all_transactions_by_user(self, user_id):
        query = "SELECT * FROM transactions WHERE user_id = ?"
        return self.fetch_all(query, (user_id,))

    # Metodă pentru a obține tranzacția după ID
    def get_transaction_by_id(self, transaction_id):
        """Obține tranzacția pe baza ID-ului."""
        query = "SELECT * FROM transactions WHERE id = ?"
        return self.fetch_one(query, (transaction_id,))

    def delete_transaction(self, transaction_id):
        """Șterge tranzacția pe baza ID-ului."""
        query = "DELETE FROM transactions WHERE id = ?"
        self.execute_query(query, (transaction_id,))