class Transaction:
    def __init__(self, uid, date, amount, category, description, transaction_type):
        # uid and name are unique
        self.__uid = uid
        self.__date = date
        self.__amount = amount
        self.__category = category
        self.__description = description
        self.__transaction_type = transaction_type

    def set_uid(self, uid):
        self.__uid = uid

    def set_date(self, date):
        self.__date = date

    def set_amount(self, amount):
        self.__amount = amount

    def set_category(self, category):
        self.__category = category

    def set_description(self, description):
        self.__description = description

    def set_transaction_type(self, transaction_type):
        self.__transaction_type = transaction_type

    # ----------------------getter-----------------------

    def get_uid(self):
        return self.__uid

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

    def __str__(self):
        return (f"Transaction\n"
                f" uid: {self.__uid}\n"
                f" date: {self.__date}\n"
                f" amount: {self.__amount}\n"
                f" category: {self.__category}\n"
                f" description: {self.__description}\n"
                f" transaction_type: {self.__transaction_type}\n")
