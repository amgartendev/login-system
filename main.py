from models import account  # type: ignore
from models import connectdb  # type: ignore
from models import email  # type: ignore
from models import token  # type: ignore
from time import sleep  # type: ignore


# TODO Create a maximum login attempts
# TODO Create a config file to store all the constants
# TODO Implement the show_infos function
# TODO Implement the change_infos functions


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


def logged_menu() -> None:
    print('======= LOGGED IN =======')
    print('(1) - Change Account Infos')
    print('(2) - Show Account Infos')
    print('(3) - Log Out')
    option: str = input('>>>: ')

    if option == '1':
        change_infos()
    elif option == '2':
        show_infos()
    elif option == '3':
        print('Logging out...')
        sleep(1)
        menu()
    else:
        print('Error: Select a valid option!')
        sleep(1)
        logged_menu()


def login() -> None:
    print('======= LOGIN =======')

    database = connectdb.ConnectDB('localhost', 'root', '', 'login_python')
    database.connect()

    user_email: str = input('Insert your email: ')
    user_password: str = input('Insert your password: ')

    if database.check_account(email=user_email, password=user_password) and database.check_account_status(user_email):
        logged_menu()
    else:
        print('Error: Invalid Credentials or Account not active!')
        print('Check if you insert your code correctly and your email matches your password...')
        sleep(2)
        menu()


def sign_up() -> None:
    print('======= SIGN UP =======')

    database: connectdb.ConnectDB = connectdb.ConnectDB('localhost', 'root', '', 'login_python')
    database.connect()

    username: str = input('Insert the username: ')
    user_email: str = input('Insert the email: ')
    user_password: str = input('Insert the password: ')

    user_account: account.Account = account.Account(user=username, email=user_email, password=user_password)

    if not user_account.check_user(username) and not user_account.check_email(user_email):
        user_account.send_account(user_account.user, user_account.email, user_account.password)

        token_obj: token.Token = token.Token()
        generated_token: str = token_obj.generate_token()
        token_obj.send_token(generated_token, user_email)

        email_obj: email.Email = email.Email()
        email_obj.send_email(user_email, generated_token)

        print("We've sent you an email with your secret code...")
        token_validation: str = input('Insert your secret code: ')

        if token_validation == generated_token:
            token_obj.activate_token(generated_token)
            print('SUCCESS!! YOU HAVE ACTIVATED YOUR ACCOUNT :)')
            sleep(2)
            menu()
        else:
            print('Error: Sorry. Your token is not valid!')
            sleep(2)
            menu()
    else:
        print('Error: User or email already taken!')
        sleep(2)
        menu()


def change_infos() -> None:
    pass


def show_infos() -> None:
    pass


if __name__ == '__main__':
    main()
