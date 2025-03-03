class Transaction:
    def __init__(self, transaction_id, date, amount, category, description, transaction_type):
        # Initialize the attributes for a transaction
        self.__transaction_id = transaction_id
        self.__date = date
        self.__amount = amount  # Using private variable to store amount
        self.__category = category
        self.__description = description
        self.__transaction_type = transaction_type  # This indicates whether it's an 'income' or 'expense'

    def __str__(self):
        # Return a string representation of the transaction
        return f"ID: {self.__transaction_id}, Date: {self.__date}, Amount: {self.__amount}, Category: {self.__category}, Description: {self.__description}, Type: {self.__transaction_type}"

    def to_dict(self):
        # Convert the transaction to a dictionary for easier database insertion or manipulation
        return {
            "transaction_id": self.__transaction_id,
            "date": self.__date,
            "amount": self.__amount,
            "category": self.__category,
            "description": self.__description,
            "transaction_type": self.__transaction_type
        }

    # ----------------------Setteri-----------------------
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_uid(self, uid):
        self.__uid = uid

    def set_date(self, date):
        self.__date = date

    def set_amount(self, amount):
        self.__amount = amount  # Correctly update the private __amount attribute

    def set_category(self, category):
        self.__category = category

    def set_description(self, description):
        self.__description = description

    def set_transaction_type(self, transaction_type):
        self.__transaction_type = transaction_type

    # ----------------------Getteri-----------------------
    def get_user_id(self):
        return getattr(self, "__user_id", None)

    def get_uid(self):
        return getattr(self, "__uid", None)

    def get_date(self):
        return self.__date

    def get_amount(self):
        return self.__amount

    def get_category(self):
        return self.__category

    def get_description(self):
        return self.__description

    def get_transaction_type(self):
        return self.__transaction_type
