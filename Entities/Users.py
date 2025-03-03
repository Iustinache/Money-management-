import sqlite3


class User:
    def __init__(self, user_id, username, password):
        self.__user_id = user_id
        self.__username = username
        self.__password = password

    # Setters
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    # Getters
    def get_user_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def __str__(self):
        return f"User ID: {self.__user_id}, Username: {self.__username}"
