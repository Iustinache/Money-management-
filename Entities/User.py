class User:
    def __init__(self, uid, name, sum, income, expenses):
        # uid and name are unique
        self.__uid = uid
        self.__name = name
        self.__sum = sum
        self.__income = income
        self.__expenses = expenses

    def set_uid(self, uid):
        self.__uid = uid

    def set_name(self, name):
        self.__name = name

    def set_sum(self, sum):
        self.__sum = sum

    def set_income(self, income):
        self.__income = income

    def set_expenses(self, expenses):
        self.__expenses = expenses

    # ----------------------getter-----------------------

    def get_uid(self):
        return self.__uid

    def get_name(self):
        return self.__name

    def get_sum(self):
        return self.__sum

    def get_income(self):
        return self.__income

    def get_expenses(self):
        return self.__expenses

    def __str__(self):
        return (f"User\n"
                f" uid: {self.__uid}\n"
                f" name: {self.__name}\n"
                f" sum: {self.__sum}\n"
                    f" income: {self.__income}\n"
                f" expenses: {self.__expenses}\n")
