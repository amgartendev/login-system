from Support import classes

# Creating the connection to the database
database = classes.ConnectDB('localhost', 'root', '', 'login_python')

print(database.connect())

token_obj = classes.Token()
token = token_obj.generate_token()

print(token)
