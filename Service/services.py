from Database.Repository import Repository
from Entities.Transaction import Transaction


class Service:
    def __init__(self, repository=None):
        # Dacă nu se specifică un repository, inițializăm unul nou implicit
        self.repository = repository if repository else Repository()

    # Metodă pentru a adăuga o tranzacție
    def add_transaction(self, user_id, transaction):
        # Validare și logică suplimentară înainte de adăugare
        if transaction.get_amount() <= 0:
            raise ValueError("Suma tranzacției trebuie să fie pozitivă.")

        transaction.set_user_id(user_id)  # Setăm user_id pentru tranzacție
        self.repository.add_transaction(user_id, transaction)

    # Metodă pentru a obține toate tranzacțiile ale unui utilizator
    def get_all_transactions_by_user(self, user_id):
        return self.repository.get_all_transactions_by_user(user_id)

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


