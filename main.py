import config
from colorama import Fore  # type: ignore
from models import account  # type: ignore
from models import connectdb  # type: ignore
from models import email  # type: ignore
from models import token  # type: ignore
from time import sleep  # type: ignore


# TODO Create a logo
# TODO Update email when user change his email in tokens table


def main() -> None:
    menu()


def menu() -> None:
    print(Fore.LIGHTBLUE_EX + '======= LOGIN SYSTEM =======')
    print(Fore.LIGHTBLUE_EX + '(1)' + Fore.RESET + ' - Login')
    print(Fore.LIGHTBLUE_EX + '(2)' + Fore.RESET + ' - Sign Up')
    print(Fore.LIGHTBLUE_EX + '(3)' + Fore.RESET + ' - Validate Token')
    print(Fore.LIGHTBLUE_EX + '(4)' + Fore.RESET + ' - Exit')
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
        print(Fore.LIGHTRED_EX + 'Error: Select a valid option!' + Fore.RESET)
        sleep(1)
        menu()


def logged_menu() -> None:
    print(Fore.LIGHTBLUE_EX + '======= LOGGED IN =======' + Fore.RESET)
    print(Fore.LIGHTBLUE_EX + '(1)' + Fore.RESET + ' - Change Account Infos')
    print(Fore.LIGHTBLUE_EX + '(2)' + Fore.RESET + ' - Show Account Infos')
    print(Fore.LIGHTBLUE_EX + '(3)' + Fore.RESET + ' - Log Out')
    option: str = input('>>>: ')

    if option == '1':
        change_infos_menu()
    elif option == '2':
        show_infos()
    elif option == '3':
        print(Fore.YELLOW + 'Logging out...' + Fore.RESET)
        sleep(1)
        menu()
    else:
        print(Fore.LIGHTRED_EX + 'Error: Select a valid option!' + Fore.RESET)
        sleep(1)
        logged_menu()


def change_infos_menu() -> None:
    print(Fore.LIGHTBLUE_EX + '======= CHANGE INFOS =======' + Fore.RESET)
    print(Fore.LIGHTBLUE_EX + '(1)' + Fore.RESET + ' - Change Username')
    print(Fore.LIGHTBLUE_EX + '(2)' + Fore.RESET + ' - Change Email')
    print(Fore.LIGHTBLUE_EX + '(3)' + Fore.RESET + ' - Change Password')
    print(Fore.LIGHTBLUE_EX + '(4)' + Fore.RESET + ' - Go Back')
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
        print(Fore.LIGHTRED_EX + 'Error: Select a valid option!' + Fore.RESET)
        sleep(2)
        logged_menu()


def login() -> None:
    print(Fore.LIGHTBLUE_EX + '======= LOGIN =======' + Fore.RESET)

    database = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    database.connect()

    user_email: str = input('Insert your email: ')
    user_password: str = input('Insert your password: ')

    if database.check_account(email=user_email, password=user_password, username=''):
        if database.check_account_status(user_email):
            logged_menu()
        else:
            print(Fore.LIGHTRED_EX + 'Error: Account not active!' + Fore.RESET)
            print(Fore.YELLOW + 'Check if you have activated your account with the token sent by your email!'
                  + Fore.RESET)
            sleep(2)
            menu()
    else:
        print(Fore.LIGHTRED_EX + 'Error: Invalid Credentials!' + Fore.RESET)
        sleep(2)
        menu()


def sign_up() -> None:
    print(Fore.LIGHTBLUE_EX + '======= SIGN UP =======' + Fore.RESET)

    database: connectdb.ConnectDB = connectdb.ConnectDB(config.DB_HOST, config.DB_USER,
                                                        config.DB_PASSWORD, config.DB_NAME)
    database.connect()

    username: str = input('Insert the username: ')
    user_email: str = input('Insert the email: ')
    user_password: str = input('Insert the password: ')

    if '@gmail.com' in user_email or '@yahoo.com' in user_email or '@hotmail.com' in user_email:
        user_account: account.Account = account.Account(user=username, email=user_email, password=user_password)

        if not user_account.check_user(username) and not user_account.check_email(user_email):
            user_account.send_account(user_account.user, user_account.email, user_account.password)

            token_obj: token.Token = token.Token()
            generated_token: str = token_obj.generate_token()
            token_obj.send_token(generated_token, user_email)

            email_obj: email.Email = email.Email()
            email_obj.send_email(user_email, generated_token)

            print(Fore.YELLOW + "We've sent you an email with your secret code..." + Fore.RESET)
            token_validation: str = input('Insert your secret code: ')

            if token_validation == generated_token:
                token_obj.activate_token(generated_token)
                print(Fore.LIGHTGREEN_EX + 'SUCCESS!! YOU HAVE ACTIVATED YOUR ACCOUNT :)' + Fore.RESET)
                email_obj.send_confirmation(user_email, user_account.user)
                sleep(2)
                menu()
            else:
                print(Fore.LIGHTRED_EX + 'Error: Sorry... Your token is not valid!' + Fore.RESET)
                sleep(2)
                menu()
        else:
            print(Fore.LIGHTRED_EX + 'Error: Username or email already taken!' + Fore.RESET)
            sleep(2)
            menu()
    else:
        print(Fore.LIGHTRED_EX + 'Error: This is not a valid email address!' + Fore.RESET)
        print(Fore.YELLOW + 'A valid email address is: @gmail.com, @yahoo.com or @hotmail.com' + Fore.RESET)
        sleep(2)
        menu()


def validate_token() -> None:
    print(Fore.LIGHTBLUE_EX + '======= VALIDATE TOKEN =======' + Fore.RESET)

    database = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    database.connect()

    token_obj = token.Token()

    user_email: str = input('Insert your email: ')
    user_token: str = input('Insert the token you want to activate: ')

    if token_obj.verify_token_owner(user_email, user_token):
        if token_obj.check_token_existence(user_token):
            if not database.check_account_status(user_email):
                token_obj.activate_token(user_token)
                print(Fore.LIGHTGREEN_EX + 'SUCCESS!! YOU HAVE ACTIVATED YOUR ACCOUNT :)' + Fore.RESET)
                sleep(2)
                menu()
            else:
                print(Fore.LIGHTGREEN_EX + 'YOUR ACCOUNT IS ALREADY ACTIVE! NO NEED TO ACTIVATE IT AGAIN' + Fore.RESET)
                sleep(2)
                menu()
        else:
            print(Fore.LIGHTRED_EX + 'Error: Sorry... Your token is not valid!' + Fore.RESET)
            sleep(2)
            menu()
    else:
        print(Fore.LIGHTRED_EX + 'Error: The token you inserted does not match your account!' + Fore.RESET)
        sleep(2)
        menu()


def change_username() -> None:
    current_username: str = input('Insert your current username: ')
    new_username: str = input('Insert your new username: ')

    if account.Account.check_user(current_username):
        if not account.Account.check_user(new_username):
            if account.Account.change_username(current_username, new_username):
                print(Fore.LIGHTGREEN_EX + f'Your username is {new_username} now!' + Fore.RESET)
                sleep(2)
                logged_menu()
            else:
                print(Fore.LIGHTRED_EX + f'Sorry, we had a problem updating your username. Try again later...'
                      + Fore.RESET)
                sleep(2)
                logged_menu()
        else:
            print(Fore.LIGHTRED_EX + 'Error: Sorry, this username is already taken!' + Fore.RESET)
            sleep(2)
            change_infos_menu()
    else:
        print(Fore.LIGHTRED_EX + 'Error: Your current username does not exist!' + Fore.RESET)
        sleep(2)
        change_infos_menu()


def change_email() -> None:
    database = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)

    email_obj = email.Email()

    token_obj = token.Token()
    generated_token = token_obj.generate_token()

    current_email: str = input('Insert your email: ')
    password_confirmation: str = input('Insert your password: ')

    if database.check_account(email=current_email, password=password_confirmation, username=''):
        print('--------------------')
        new_email: str = input('Insert your new email: ')
        if '@gmail.com' in new_email or '@yahoo.com' in new_email or '@hotmail.com' in new_email:
            if account.Account.change_email(current_email, new_email):
                email_obj.send_change_confirmation(current_email, generated_token)
                token_obj.deactivate_token(current_email, generated_token)
                print(Fore.YELLOW + 'Now you need to activate your account again...' + Fore.RESET)
                print(Fore.YELLOW + "We've sent you an email with your secret code..." + Fore.RESET)
                print(Fore.YELLOW + 'Go to the menu and select the option "(3) - Validate Token" and'
                                    ' insert your new token!' + Fore.RESET)

                sleep(3)
                logged_menu()
            else:
                print(Fore.LIGHTRED_EX + f'Sorry, we had a problem updating your email. Try again later...'
                      + Fore.RESET)
                sleep(2)
                logged_menu()
        else:
            print(Fore.LIGHTRED_EX + 'Error: This is not a valid email address!' + Fore.RESET)
            print(Fore.YELLOW + 'A valid email address is: @gmail.com, @yahoo.com or @hotmail.com' + Fore.RESET)
            sleep(2)
            logged_menu()
    else:
        print(Fore.LIGHTRED_EX + 'Error: This username does not match this password!' + Fore.RESET)
        sleep(2)
        logged_menu()


def change_password() -> None:
    database = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)

    username: str = input('Insert your username: ')
    password_confirmation: str = input('Insert your password: ')

    if database.check_account(email='', username=username, password=password_confirmation, by_username=True):
        print('--------------------')
        new_password: str = input('Insert your new password: ')
        new_password_confirmation: str = input('Confirm your new password: ')

        if new_password == new_password_confirmation:
            if account.Account.change_password(new_password, username):
                print(Fore.LIGHTGREEN_EX + f"You've updated your password!" + Fore.RESET)
                sleep(2)
                logged_menu()
            else:
                print(Fore.LIGHTRED_EX + f'Sorry, we had a problem updating your password. Try again later...'
                      + Fore.RESET)
                sleep(2)
                logged_menu()
        else:
            print(Fore.LIGHTRED_EX + 'Error: The passwords does not match!' + Fore.RESET)
            sleep(2)
            logged_menu()
    else:
        print(Fore.LIGHTRED_EX + 'Error: This username does not match this password!' + Fore.RESET)
        sleep(2)
        logged_menu()


def show_infos() -> None:
    database = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)

    user: str = input('Insert your username: ')
    if database.return_account_infos(user):
        print(database.return_account_infos(user))
        logged_menu()
    else:
        print(Fore.LIGHTRED_EX + 'Error: This username does not exist!' + Fore.RESET)
        sleep(2)
        logged_menu()


if __name__ == '__main__':
    main()
