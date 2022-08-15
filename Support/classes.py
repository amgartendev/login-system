import mysql.connector  # type: ignore
import smtplib
from random import choice
from email.message import EmailMessage
from typing import Union


class ConnectDB:
    def __init__(self, dbhost: str, dbuser: str, dbpassword: str, dbname: str) -> None:
        self.__dbhost = dbhost
        self.__dbuser = dbuser
        self.__dbpassword = dbpassword
        self.__dbname = dbname

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__dbhost}, {self.__dbuser}, {self.__dbpassword}, {self.__dbname})'

    @property
    def host(self) -> str:
        return self.__dbhost

    @property
    def user(self) -> str:
        return self.__dbuser

    @property
    def name(self) -> str:
        return self.__dbname

    def connect(self):
        """Tries to connect to the database"""
        try:
            db = mysql.connector.connect(
                host=self.__dbhost,
                user=self.__dbuser,
                password=self.__dbpassword,
                database=self.__dbname
            )
            return db
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    def return_infos(self, table: str) -> list:
        """Return all the occurrences of the specified table"""
        db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM {table}"
        cursor.execute(sql)
        result = cursor.fetchall()  # Fetch all rows from database table
        print(f'{len(result)} result(s) found in {table}!')
        return result

    def check_user(self, user: str) -> bool:
        """Check if the user is already taken and return True"""
        db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM accounts WHERE user='{user}'"
        cursor.execute(sql)
        rows = cursor.fetchall()  # Fetch all rows from database table

        # Check if one or more users were find in the database with the same user passed as argument
        if len(rows) > 0:
            return True  # User already taken
        return False

    def check_email(self, email: str) -> bool:
        """Check if the email is already taken and return True"""
        db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM accounts WHERE email='{email}'"
        cursor.execute(sql)
        rows = cursor.fetchall()  # Fetch all rows from database table

        # Check if one or more emails were find in the database with the same email passed as argument
        if len(rows) > 0:
            return True  # Email already taken
        return False

    def check_account(self, email: str, password: str) -> bool:
        """Check if the account exists in the database and return True"""
        db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM accounts WHERE email='{email}' AND password='{password}'"
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Check if the email and password passed as argument is registered in the database
        if len(rows) > 0:
            return True
        return False

    def send_account(self, *args) -> Union[bool, str]:
        """Send account details to the database"""

        account = tuple(args)

        try:
            db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"INSERT INTO accounts (user, email, password) " \
                  f"VALUES ('{account[0]}', '{account[1]}', '{account[2]}')"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    def send_token(self, token: str) -> Union[bool, str]:
        """Send token to the database and set it as inactive by default"""
        try:
            db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"INSERT INTO tokens (token, active) VALUES ('{token}', '0')"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'


class Token:
    def __init__(self) -> None:
        pass

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
    def activate_token(token: str) -> Union[bool, str]:
        """Set token column in the database as 1 (active) and return True"""
        try:
            db = ConnectDB('localhost', 'root', '', 'login_python')
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"UPDATE tokens SET active='1' WHERE token='{token}'"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'


class Email:
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} Class'

    @staticmethod
    def send_email(receiver: str, token: str) -> bool:
        """Send an email with the authentication token"""
        email_sender = 'your_email_here@gmail.com'  # Your Google account here
        email_password = 'you_app_password_here'  # Your app password here
        email_receiver = receiver

        msg = EmailMessage()
        msg['Subject'] = 'Your Activation Token'
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg.set_content(f'Thanks for joining us\n{token}')
        msg.add_alternative(f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1 style="color:#047BBF; text-align:center;">Thanks for joining us</h1>
                <h1 style="text-align:center;">Your acess token:<br>{token}</h1>
            </body>
        </html>
        """, subtype='html')

        try:
            # Gmail -> smtp.gmail.com
            # Hotmail -> smtp.live.com
            # Yahoo -> smtp.mail.yahoo.com
            with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()  # Encrypting our connection to the server
                connection.login(email_sender, email_password)
                connection.send_message(msg)
                return True
        except smtplib.SMTPAuthenticationError as errorMsg:
            print(f"Error: {errorMsg}")
            return False


class Account:
    def __init__(self, user: str, email: str, password: str) -> None:
        self.__user = user
        self.__email = email
        self.__password = password

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
