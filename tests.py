from Support import classes

# Creating the connection to the database
database = classes.ConnectDB('localhost', 'root', '', 'login_python')
database.connect()

token_obj = classes.Token()
token = token_obj.generate_token()

acc = classes.Account('joao', 'joao@gmail.com', '87312')

email = classes.Email()


# Testing Attributes
print('======== TESTING ATTRIBUTES ========')
print(f"host attr: {database.host}")
print(f"user attr: {database.user}")
print(f"name attr: {database.name}")
print(f"user attr: {acc.user}")
print(f"email attr: {acc.email}")

# Testing Methods
print('\n======== TESTING METHODS ========')
print(f"ConnectDB __repr__: {database}")
print(f"return_infos(account): {database.return_infos('accounts')}\n")
print(f"return_infos(tokens): {database.return_infos('tokens')}\n")
print(f"check_user(amgarten): {database.check_user('amgarten')}\n")
print(f"check_email(amgarten@gmail.com): {database.check_email('amgarten@gmail.com')}\n")
# print(f"send_account: {database.send_account(('Teste', 'teste@gmail.com', '231'))}")
print(f"Token __repr__: {token_obj}\n")
print(f"generate_token: {token}\n")
print(f"send_token(token): {database.send_token(token)}\n")
print(f"Account __repr__: {acc}\n")
print(f"{database.send_account(acc.user, acc.email, acc.password)}\n")
print(f"activate_token(token): {token_obj.activate_token('1e144')}\n")
print(f"check_account(email, password): {database.check_account('testaccount@gmail.com', '2005')}\n")
print(email.send_email('new_account_registration_here@gmail.com', token))
