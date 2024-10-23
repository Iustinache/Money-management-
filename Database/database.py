import sqlite3


def setup_database():
    conn = sqlite3.connect('finance.db')
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


def add_to_db(transaction):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Inserarea tranzactiei in baza de date
    cursor.execute('''
        INSERT INTO transactions (date,amount,category, description,transactoin_type)
        VALUES (?,?,?,?,?)
    ''', (transaction.get_date(), transaction.get_amount(), transaction.get_category(), transaction.get_description(), transaction.get_transaction_type()))
    conn.commit()
    conn.close()

def get_all_transaction():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    #Obtinerea tuturor tranzactiilor

    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()

    conn.close()
    return transactions

