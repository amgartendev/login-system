import config
import mysql.connector  # type: ignore
from models import connectdb  # type: ignore
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
            db = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"INSERT INTO tokens (token, email, active) VALUES ('{token}', '{email}', '0')"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    @staticmethod
    def check_token_existence(token: str) -> Union[bool, str]:
        """Check if the token inserted by the user exists in the database"""
        try:
            db = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"SELECT * FROM tokens WHERE token='{token}'"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if len(rows) > 0:
                return True
            return False
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    @staticmethod
    def verify_token_owner(email: str, token: str) -> Union[bool, str]:
        """Check by email if the token inserted is the same in the database"""
        try:
            db = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"SELECT * FROM tokens WHERE email='{email}' AND token='{token}'"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if len(rows) > 0:
                return True
            return False
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    @staticmethod
    def activate_token(token: str) -> Union[bool, str]:
        """Set token column in the database as 1 (active) and return True"""
        try:
            db = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"UPDATE tokens SET active='1' WHERE token='{token}'"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    @staticmethod
    def deactivate_token(old_email: str, token: str) -> Union[bool, str]:
        """Set token column in the database as 0 (inactive) and return True"""
        try:
            db = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
            conn = db.connect()
            cursor = conn.cursor()

            sql_change_token = f"UPDATE tokens SET token='{token}' WHERE email='{old_email}'"
            cursor.execute(sql_change_token)

            sql_set_account_as_inactive = f"UPDATE tokens SET active='0' WHERE email='{old_email}'"
            cursor.execute(sql_set_account_as_inactive)

            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'
