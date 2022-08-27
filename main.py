import config
from models import account  # type: ignore
from models import connectdb  # type: ignore
from models import email  # type: ignore
from models import token  # type: ignore
from time import sleep  # type: ignore


# TODO Create a maximum login attempts
# TODO Implement the change_username() method in account.py
# TODO Implement the change_email() method in account.py
# TODO Implement the change_password() method in account.py
# TODO Create a logo
# TODO Fix List Index Out Of Range when returning an invalid username in show_infos()
# TODO Create a new boolean parameter in check_account() method named "by_user"
# TODO Use the parameter "by_user" in check_account() in functions change_username() and change_password()
# TODO Create a new email template when user change the email and set the "active" table in the database as 0
# TODO Use the new email template in line 188
# TODO Make sure that the new token is updated in the database when user use the change_email() function


def main() -> None:
    menu()


def menu() -> None:
    print('======= LOGIN SYSTEM =======')
    print('(1) - Login')
    print('(2) - Sign Up')
    print('(3) - Validate Token')
    print('(4) - Exit')
    option: str = input('>>>: ')

    if option == '1':
        login()
    elif option == '2':
        sign_up()
    elif option == '3':
        validate_token()
    elif option == '4':
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
        change_infos_menu()
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


def change_infos_menu() -> None:
    print('======= CHANGE INFOS =======')
    print('(1) - Change Username')
    print('(2) - Change Email')
    print('(3) - Change Password')
    print('(4) - Go Back')
    option: str = input('>>>: ')

    if option == '1':
        change_username()
    elif option == '2':
        change_email()
    elif option == '3':
        change_password()
    elif option == '4':
        logged_menu()
    else:
        print('Error: Select a valid option!')
        sleep(2)
        logged_menu()


def login() -> None:
    print('======= LOGIN =======')

    database = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
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

    database: connectdb.ConnectDB = connectdb.ConnectDB(config.DB_HOST, config.DB_USER,
                                                        config.DB_PASSWORD, config.DB_NAME)
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
            email_obj.send_confirmation(user_email, user_account.user)
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


def validate_token() -> None:
    pass


def change_username() -> None:
    current_username: str = input('Insert your current username: ')
    new_username: str = input('Insert your new username: ')

    if not account.Account.check_user(new_username):
        if account.Account.change_username(current_username, new_username):
            print(f'Your username is {new_username} now!')
            sleep(2)
            logged_menu()
        else:
            print(f'Sorry, we had a problem updating your username. Try again later...')
            sleep(2)
            logged_menu()
    else:
        print('Error: Sorry, this username is already taken!')
        sleep(2)
        change_infos_menu()


def change_email() -> None:
    database = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)

    email_obj = email.Email()

    token_obj = token.Token()
    generated_token = token_obj.generate_token()

    username: str = input('Insert your email: ')
    password_confirmation: str = input('Insert your password: ')

    if database.check_account(username, password_confirmation):
        print('--------------------')
        new_email: str = input('Insert your new email: ')
        if account.Account.change_email():
            email_obj.send_email(new_email, generated_token)
            print('Now you need to activate your account again...')
            print("We've sent you an email with your secret code...")
            print('Go to the menu and select the option "(3) - Validate Token" and insert your new token!')
            sleep(3)
            logged_menu()
        else:
            print(f'Sorry, we had a problem updating your email. Try again later...')
            sleep(2)
            logged_menu()
    else:
        print('Error: This username does not match this password!')
        sleep(2)
        logged_menu()


def change_password() -> None:
    database = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)

    username: str = input('Insert your email: ')
    password_confirmation: str = input('Insert your password: ')

    if database.check_account(username, password_confirmation):
        print('--------------------')
        new_password: str = input('Insert your new password: ')
        new_password_confirmation: str = input('Confirm your new password: ')

        if new_password == new_password_confirmation:
            if account.Account.change_password(username, new_password):
                print(f"You've updated your password!")
                sleep(2)
                logged_menu()
            else:
                print(f'Sorry, we had a problem updating your password. Try again later...')
                sleep(2)
                logged_menu()
        else:
            print('Error: The passwords does not match!')
            sleep(2)
            logged_menu()
    else:
        print('Error: This username does not match this password!')
        sleep(2)
        logged_menu()


def show_infos() -> None:
    database = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)

    user: str = input('Insert your username: ')
    if database.return_account_infos(user):
        print(database.return_account_infos(user))
        logged_menu()
    else:
        print('Error: This username does not exist!')
        sleep(2)
        logged_menu()


if __name__ == '__main__':
    main()
