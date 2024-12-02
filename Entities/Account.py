class User:
    def __init__(self, uid, email, password):
        # uid and name are unique
        self.__uid = uid
        self.__email = email
        self.__password = password

    def set_uid(self, uid):
        self.__uid = uid

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    # ----------------------getter-----------------------

    def get_uid(self):
        return self.__uid

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def __str__(self):
        return (f"Account\n"
                f" uid: {self.__uid}\n"
                f" email: {self.__email}\n")
