from models import account  # type: ignore
from models import connectdb  # type: ignore
from models import email  # type: ignore
from models import token  # type: ignore
from time import sleep  # type: ignore


def main() -> None:
    menu()


def menu() -> None:
    print('======= LOGIN SYSTEM =======')
    print('(1) - Login')
    print('(2) - Sign Up')
    print('(3) - Exit')
    option: str = input('>>>: ')

    if option == '1':
        login()
    elif option == '2':
        sign_up()
    elif option == '3':
        print('Bye Bye...')
        exit(0)
    else:
        print('Error: Select a valid option!')
        sleep(1)
        menu()


def login() -> None:
    print('======= LOGIN =======')

    database = connectdb.ConnectDB('localhost', 'root', '', 'login_python')
    database.connect()

    user_email: str = input('Insert your email: ')
    user_password: str = input('Insert your password: ')

    if database.check_account(email=user_email, password=user_password):
        print('LOGGED IN')
    else:
        print('Error: Invalid Credentials')
        sleep(2)
        menu()


def sign_up():
    pass


if __name__ == '__main__':
    main()
