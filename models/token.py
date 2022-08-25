from models import connectdb  # type: ignore
import mysql.connector  # type: ignore
from random import choice
from typing import Union


class Token:
    def __repr__(self) -> str:
        return f'{self.__class__.__name__} Class'

    @staticmethod
    def generate_token() -> str:
        """Creates a token with 759.375 different combinations and return it"""
        chars = ['a', 'b', 'c', 'd', 'e', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        token = ''

        for i in range(5):
            token += str(choice(chars))
        return token

    @staticmethod
    def send_token(token: str, email: str) -> Union[bool, str]:
        """Send token to the database and set it as inactive by default"""
        try:
            db = connectdb.ConnectDB('localhost', 'root', '', 'login_python')
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"INSERT INTO tokens (token, email, active) VALUES ('{token}', '{email}', '0')"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    @staticmethod
    def activate_token(token: str) -> Union[bool, str]:
        """Set token column in the database as 1 (active) and return True"""
        try:
            db = connectdb.ConnectDB('localhost', 'root', '', 'login_python')
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"UPDATE tokens SET active='1' WHERE token='{token}'"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'
