from Support import classes

# TODO Add Change Infos option
# TODO Add a configuration file with important constants


print('===== LOGIN SYSTEM =====')
print('(1) - Log In')
print('(2) - Sign Up')
print('(3) - Exit')
option = input('>>>: ').strip()

while option != '1' and option != '2' and option != '3':
    print('Error: Choose an valid option!')
    option = input('>>>: ').strip()

if option == '1':
    database = classes.ConnectDB('localhost', 'root', '', 'login_python')
    login_attempts = 0

    while True:
        if login_attempts == 3:
            print('Sorry... you tried to log in too many times. Try again later!')
            exit()

        email = input('Insert your email: ').strip()
        password = input('Insert your password: ').strip()

        if database.check_account(email, password):
            print(f'Logged in!!')
            break
        else:
            print('Email or password not valid!!')
            login_attempts += 1
elif option == '2':
    pass
else:
    print('Bye Bye...')
    exit()
