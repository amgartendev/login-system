import config
from models import account
from models import connectdb
from models import email
from models import token


acc1 = account.Account('Joao', 'joao@gmail.com', '123')
print("=========== TESTING ACCOUNT ===========")
print(f"__repr__: {acc1}")
print(f"user: {acc1.user}")
print(f"email: {acc1.email}")
print(f"password: {acc1.password}")
print(f"check_user(): {acc1.check_user('joao')}")
print(f"check_email(): {acc1.check_email('joao@gmail.com')}")
print(f"send_account(): {acc1.send_account(acc1.user, acc1.email, acc1.password)}")


db1 = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
print("\n=========== TESTING CONNECTDB ===========")
print(f"__repr__: {db1}")
print(f"host: {db1.host}")
print(f"user: {db1.user}")
print(f"name: {db1.name}")
print(f"connect(): {db1.connect()}")
print(f"return_infos(): {db1.return_table_infos('tokens')}")
print(f"check_account() Expect False: {db1.check_account('joao@gmail.com', '1234')}")  # Expected: False
print(f"check_account() Expect True: {db1.check_account('joao@gmail.com', '87312')}")  # Expected: True


email = email.Email()
print("\n=========== TESTING EMAIL ===========")
print(f"__repr__: {email}")
print(f"send_email(): {email.send_email('new_account_registration_here@gmail.com', '123')}")


token = token.Token()
print("\n=========== TESTING TOKEN ===========")
print(f"__repr__: {token}")
print(f"generate_token(): {token.generate_token()}")
print(f"send_token(): {token.send_token('123', acc1.email)}")
print(f"activate_token(): {token.activate_token('123')}")
