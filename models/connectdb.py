import mysql.connector  # type: ignore


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
