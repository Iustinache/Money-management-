from Entities.Transaction import Transaction

transactions = []
def add_transactions(uid, date, amount, category, description, transaction_type):
    transaction = Transaction(uid, date, amount, category, description, transaction_type)
    transactions.append(transaction)

def get_balace():
    income = sum(t.amount for t in transactions if t.get_transaction_type() == "income")
    expenses = sum(t.amount for t in transactions if t.get_transaction_type() == "expenses")
    return income-expenses

