import mysql.connector  # type: ignore
from typing import Union


class ConnectDB:
    def __init__(self: object, dbhost: str, dbuser: str, dbpassword: str, dbname: str) -> None:
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

    def return_table_infos(self, table: str) -> list:
        """Return all the occurrences of the specified table"""
        db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM {table}"
        cursor.execute(sql)
        result = cursor.fetchall()  # Fetch all rows from database table
        print(f'{len(result)} result(s) found in {table}!')
        return result

    def return_account_infos(self, user: str) -> Union[str, bool]:
        db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM accounts where user='{user}'"
        cursor.execute(sql)
        rows = cursor.fetchall()

        infos = f"Username: {rows[0][1]}\nEmail: {rows[0][2]}\nPassword: {rows[0][3]}"

        if len(rows) > 0:
            return infos
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

    def check_account_status(self, email: str) -> bool:
        """Check if the account is active by checking the 'active' column in the table 'tokens' in the database"""
        db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM tokens WHERE email='{email}' AND active='1'"
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Check if the account is activated with the token
        if len(rows) > 0:
            return True
        return False
