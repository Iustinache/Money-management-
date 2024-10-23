class Transaction:
    def __init__(self, uid, date, sum, category, description, type):
        # uid and name are unique
        self.__uid = uid
        self.__date = date
        self.__sum = sum
        self.__category = category
        self.__description = description
        self.__type = type

    def set_uid(self, uid):
        self.__uid = uid

    def set_date(self, date):
        self.__date = date

    def set_sum(self, sum):
        self.__sum = sum

    def set_category(self, category):
        self.__category = category

    def set_description(self, description):
        self.__description = description

    def set_type(self, type):
        self.__type = type

    # ----------------------getter-----------------------

    def get_uid(self):
        return self.__uid

    def get_date(self):
        return self.__date

    def get_sum(self):
        return self.__sum

    def get_category(self):
        return self.__category

    def get_description(self):
        return self.__description

    def get_type(self):
        return self.__type

    def __str__(self):
        return f"Transaction\n uid: {self.__uid}\n"
