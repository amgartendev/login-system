from models import connectdb  # type: ignore
import mysql.connector  # type: ignore
from typing import Union


class Account:
    def __init__(self, user: str, email: str, password: str) -> None:
        self.__user: str = user
        self.__email: str = email
        self.__password: str = password

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__user}, {self.__email}, {self.__password})'

    @property
    def user(self) -> str:
        return self.__user

    @property
    def email(self) -> str:
        return self.__email

    @property
    def password(self) -> str:
        return self.__password

    @staticmethod
    def check_user(user: str) -> bool:
        """Check if the user is already taken and return True"""
        db = connectdb.ConnectDB('localhost', 'root', '', 'login_python')
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM accounts WHERE user='{user}'"
        cursor.execute(sql)
        rows = cursor.fetchall()  # Fetch all rows from database table

        # Check if one or more users were find in the database with the same user passed as argument
        if len(rows) > 0:
            return True  # User already taken
        return False

    @staticmethod
    def check_email(email: str) -> bool:
        """Check if the email is already taken and return True"""
        db = connectdb.ConnectDB('localhost', 'root', '', 'login_python')
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM accounts WHERE email='{email}'"
        cursor.execute(sql)
        rows = cursor.fetchall()  # Fetch all rows from database table

        # Check if one or more emails were find in the database with the same email passed as argument
        if len(rows) > 0:
            return True  # Email already taken
        return False

    @staticmethod
    def check_account(email: str, password: str) -> bool:
        """Check if the account exists in the database and return True"""
        db = connectdb.ConnectDB('localhost', 'root', '', 'login_python')
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM accounts WHERE email='{email}' AND password='{password}'"
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Check if the email and password passed as argument is registered in the database
        if len(rows) > 0:
            return True
        return False

    @staticmethod
    def send_account(*args) -> Union[bool, str]:
        """Send account details to the database"""

        account = tuple(args)

        try:
            db = connectdb.ConnectDB('localhost', 'root', '', 'login_python')
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"INSERT INTO accounts (user, email, password) " \
                  f"VALUES ('{account[0]}', '{account[1]}', '{account[2]}')"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'
