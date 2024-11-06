import sqlite3

import sqlite3


class Repository:
    def __init__(self, db_name='finance.db'):
        self.db_name = db_name
        self.setup_database()

    # Configurare și creare tabele necesare
    def setup_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                amount REAL,
                category TEXT,
                description TEXT,
                transaction_type TEXT
            )
        ''')
        conn.commit()
        conn.close()

    # Adăugare tranzacție în baza de date
    def add_transaction(self, transaction):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO transactions (date, amount, category, description, transaction_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (transaction.get_date(), transaction.get_amount(), transaction.get_category(),
              transaction.get_description(), transaction.get_transaction_type()))

        conn.commit()
        conn.close()

    # Obținere toate tranzacțiile
    def get_all_transactions(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM transactions')
        transactions = cursor.fetchall()

        conn.close()
        return transactions

    # Obținere tranzacție după ID
    def get_transaction_by_id(self, transaction_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
        transaction = cursor.fetchone()

        conn.close()
        return transaction

    # Actualizare tranzacție
    def update_transaction(self, transaction_id, updated_transaction):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE transactions
            SET date = ?, amount = ?, category = ?, description = ?, transaction_type = ?
            WHERE id = ?
        ''', (updated_transaction.get_date(), updated_transaction.get_amount(),
              updated_transaction.get_category(), updated_transaction.get_description(),
              updated_transaction.get_transaction_type(), transaction_id))

        conn.commit()
        conn.close()

    # Ștergere tranzacție după ID
    def delete_transaction(self, transaction_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))

        conn.commit()
        conn.close()


# def setup_database():
#     conn = sqlite3.connect('finance.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS transactions(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             date TEXT,
#             amount REAL,
#             category TEXT,
#             description TEXT,
#             transaction_type TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()
#
#
# def add_to_db(transaction):
#     conn = sqlite3.connect('finance.db')
#     cursor = conn.cursor()
#
#     # Inserarea tranzactiei in baza de date
#     cursor.execute('''
#         INSERT INTO transactions (date,amount,category, description,transactoin_type)
#         VALUES (?,?,?,?,?)
#     ''', (transaction.get_date(), transaction.get_amount(), transaction.get_category(), transaction.get_description(), transaction.get_transaction_type()))
#     conn.commit()
#     conn.close()
#
# def get_all_transaction():
#     conn = sqlite3.connect('finance.db')
#     cursor = conn.cursor()
#
#     #Obtinerea tuturor tranzactiilor
#
#     cursor.execute('SELECT * FROM transactions')
#     transactions = cursor.fetchall()
#
#     conn.close()
#     return transactions
#
