import sqlite3


class Repository:
    def __init__(self, db_name="finance.db"):
        self.db_name = db_name
        self.setup_database()

    # Configurare și creare tabele necesare
    def setup_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Crearea tabelei pentru utilizatori
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Crearea tabelei pentru tranzacții cu referință la user_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT,
                amount REAL,
                category TEXT,
                description TEXT,
                transaction_type TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()

    # Adăugare utilizator
    def add_user(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, password))

        conn.commit()
        conn.close()

    # Adăugare tranzacție cu user_id
    def add_transaction(self, user_id, transaction):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO transactions (user_id, date, amount, category, description, transaction_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, transaction.get_date(), transaction.get_amount(),
              transaction.get_category(), transaction.get_description(),
              transaction.get_transaction_type()))

        conn.commit()
        conn.close()

    # Obținere toate tranzacțiile unui utilizator
    def get_transactions_by_user(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
        transactions = cursor.fetchall()

        conn.close()
        return transactions

    # Obținere utilizator după username
    def get_user_by_username(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        conn.close()
        return user

