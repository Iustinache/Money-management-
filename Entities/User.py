class User:
    def __init__(self, uid, name, sum, income, expenses, email, password):
        # uid and name are unique
        self.__uid = uid
        self.__name = name
        self.__sum = sum
        self.__income = income
        self.__expenses = expenses
        self.__email = email
        self.__password = password

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

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

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

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def __str__(self):
        return (f"User\n"
                f" uid: {self.__uid}\n"
                f" name: {self.__name}\n"
                f" sum: {self.__sum}\n"
                f" income: {self.__income}\n"
                f" expenses: {self.__expenses}\n"
                f" email: {self.__email}\n"
                f" password: {self.__password}")
