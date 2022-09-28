<a href="https:/github.com/amgartendev/unlocked-login-system"><img src="https://i.ibb.co/g9VVDdY/unlockedf.png" width="125" height="125" align="right" /></a>

# UNLOCKED - Login System

UNLOCKED is a Python program that simulates a real login system with
database connection through a localhost server.

UNLOCKED comes with login, account creation, email and token validation.
The program was created using OOP, Type Hints and the PEP8, so if you
have any PR, please follow these development pattern.


## 💬 How can you help the project?

If you have any Bug Report you can use this link below to report all
the bugs you find.

| Type                            | Links                              |
|---------------------------------|-----------------------------------------|
| ✅ **Pull Requests**           |  <b><a href="https://github.com/amgartendev/unlocked-login-system/pulls">Send your Pull Request</a>|
| 🚨 **Bug Reports**              | <b><a href="https://github.com/amgartendev/unlocked-login-system/issues">Send your Bug Report</a>|


## 💻 UNLOCKED Works in

This is all the platforms that I've tested the app and it's working so far.
If your platform is not listed here it was not tested yet.

| Platform | Status      | Lastest Python Version Tested |
|----------|-------------|-------------------------------|
| PyCharm  | ✅ Working |             3.10.7            |
| VS Code  | ✅ Working |             3.10.7            | 
| CMD      | ✅ Working |             3.10.7            |


## 📦 Install and Set Up UNLOCKED

The current version of the project was created on Windows using PyCharm
and was not tested in any other operating system until now.

Follow the steps below to install all the packages necessary to use
UNLOCKED:

Packages needed:
```bash
pip install --upgrade pip
pip install colorama
pip install mysql-connector
```

----  
### 💾 Setting up the Data Base:

This is the database structure, make sure to create all the tables and fields correctly.

<img src="https://i.ibb.co/g3DQ8Kk/unknown.png" />

Account table structure:

<img src="https://i.ibb.co/F7V9J5t/unknown.png" />

Token table structure:

<img src="https://i.ibb.co/n7jxvcV/unknown.png" />  

----
### 🌐 Setting up your Google Account

To send and receive emails using Python, we need to make some changes in our google account.  

1º - Go to your Google Account by <a href="https://myaccount.google.com/?hl=en_UK" target="_blank">clicking here</a>  

On the top left you will see a panel like this one

<img src="https://i.ibb.co/hc0kz5w/Screenshot-2.png" height="300" />  
  
2º - Select "Security"  
  
<img src="https://i.ibb.co/QbjwFTD/Screenshot-1.png" height="300" />  

3º - Enable the Second Step Verification
  
<img src="https://i.ibb.co/8gzVTG6/Screenshot-3.png" />

4º - A new option named "Apps password" will pop up. Select it  
  
<img src="https://i.ibb.co/TPCf7ST/Screenshot-4.png"  />
  
5º - Select "Other (Custom Name)" in "Select App" 
  
<img src="https://i.ibb.co/G3Bn1sB/Screenshot-5.png" />
  
6º - Name it whatever you want and click "Generate"  
  
<img src="https://i.ibb.co/7Jw4s2j/Screenshot-6.png" />  
  
7º - ⚠️ SAVE YOUR PASSWORD ⚠️  
  
<img src="https://i.ibb.co/QX4sZbz/Screenshot-7.png" />  
  
----
### 🐍 Setting up Python's Constants
You can find all the constants in the "config.py" file  
  
1º Changing the database constants  
  
You can change this if you have a different database configuration.    
But for localhost this is pretty much it

<img src="https://i.ibb.co/ZdMP5mp/Screenshot-8.png" />
  
2º Changing the email constants  
  
Change the value of "EMAIL_SENDER" constant to the email that you created your App Password  
And the "EMAIL_PASSWORD" to the App Password that I told you to save it for later  
  
<img src="https://i.ibb.co/cg1Nrbj/Screenshot-9.png" />
