from Database.database import Repository
from Entities.Transaction import Transaction



class Service:
    def __init__(self, repository=None):
        # Dacă nu se specifică un repository, inițializăm unul nou implicit
        self.repository = repository if repository else Repository()

    # Metodă pentru a adăuga o tranzacție
    def add_transaction(self, transaction):
        # Validare și logică suplimentară înainte de adăugare, dacă e necesar
        if transaction.get_amount() <= 0:
            raise ValueError("Suma tranzacției trebuie să fie pozitivă.")

        self.repository.add_transaction(transaction)

    # Metodă pentru a obține toate tranzacțiile
    def get_all_transactions(self):
        return self.repository.get_all_transactions()

    # Metodă pentru a obține o tranzacție specifică după ID
    def get_transaction_by_id(self, transaction_id):
        transaction = self.repository.get_transaction_by_id(transaction_id)
        if transaction is None:
            raise ValueError("Tranzacția nu există.")
        return transaction

    # Metodă pentru a actualiza o tranzacție
    def update_transaction(self, transaction_id, updated_transaction):
        # Verifică dacă tranzacția există înainte de actualizare
        existing_transaction = self.get_transaction_by_id(transaction_id)
        if existing_transaction is None:
            raise ValueError("Tranzacția nu există și nu poate fi actualizată.")

        self.repository.update_transaction(transaction_id, updated_transaction)

    # Metodă pentru a șterge o tranzacție
    def delete_transaction(self, transaction_id):
        # Verifică dacă tranzacția există înainte de ștergere
        existing_transaction = self.get_transaction_by_id(transaction_id)
        if existing_transaction is None:
            raise ValueError("Tranzacția nu există și nu poate fi ștearsă.")

        self.repository.delete_transaction(transaction_id)

# transactions = []
# def add_transactions(uid, date, amount, category, description, transaction_type):
#     transaction = Transaction(uid, date, amount, category, description, transaction_type)
#     transactions.append(transaction)
#
# def get_balace():
#     income = sum(t.amount for t in transactions if t.get_transaction_type() == "income")
#     expenses = sum(t.amount for t in transactions if t.get_transaction_type() == "expenses")
#     return income-expenses

