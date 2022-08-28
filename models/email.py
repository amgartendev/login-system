import config
import smtplib
from email.message import EmailMessage


class Email:
    def __repr__(self) -> str:
        return f'{self.__class__.__name__} Class'

    @staticmethod
    def send_email(receiver: str, token: str) -> bool:
        """Send an email with the authentication token"""
        email_sender = config.EMAIL_SENDER  # Your Google account here
        email_password = config.EMAIL_PASSWORD  # Your app password here
        email_receiver = receiver

        msg = EmailMessage()
        msg['Subject'] = 'Your Activation Token'
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg.set_content(f'Thanks for joining us\n{token}')
        msg.add_alternative(f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1 style="color:#047BBF; text-align:center;">Thanks for joining us</h1>
                <h1 style="text-align:center;">Your acess token:<br>{token}</h1>
            </body>
        </html>
        """, subtype='html')

        try:
            # Gmail -> smtp.gmail.com
            # Hotmail -> smtp.live.com
            # Yahoo -> smtp.mail.yahoo.com
            with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()  # Encrypting our connection to the server
                connection.login(email_sender, email_password)
                connection.send_message(msg)
                return True
        except smtplib.SMTPAuthenticationError as errorMsg:
            print(f"Error: {errorMsg}")
            return False

    @staticmethod
    def send_confirmation(receiver: str, name: str) -> bool:
        """Send an email confirming that your account is active"""
        email_sender = config.EMAIL_SENDER  # Your Google account here
        email_password = config.EMAIL_PASSWORD  # Your app password here
        email_receiver = receiver

        msg = EmailMessage()
        msg['Subject'] = 'YOUR ACCOUNT IS ACTIVE!'
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg.set_content(f'YOUR ACCOUNT IS NOW ACTIVE!\nEnjoy using our app, {name}')
        msg.add_alternative(f"""\
                <!DOCTYPE html>
                <html>
                    <body>
                        <h1 style="color:#047BBF; text-align:center;">YOUR ACCOUNT IS NOW ACTIVE</h1>
                        <h1 style="text-align:center;">Enjoy using our app, {name}</h1>
                    </body>
                </html>
                """, subtype='html')

        try:
            # Gmail -> smtp.gmail.com
            # Hotmail -> smtp.live.com
            # Yahoo -> smtp.mail.yahoo.com
            with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()  # Encrypting our connection to the server
                connection.login(email_sender, email_password)
                connection.send_message(msg)
                return True
        except smtplib.SMTPAuthenticationError as errorMsg:
            print(f"Error: {errorMsg}")
            return False

    @staticmethod
    def send_change_confirmation(receiver: str, token: str) -> bool:
        """Send an email confirming that the user truly wants to change his email"""
        email_sender = config.EMAIL_SENDER  # Your Google account here
        email_password = config.EMAIL_PASSWORD  # Your app password here
        email_receiver = receiver

        msg = EmailMessage()
        msg['Subject'] = 'YOUR ACCOUNT IS ACTIVE!'
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg.set_content(f'CONFIRM YOUR NEW EMAIL')
        msg.add_alternative(f"""\
                        <!DOCTYPE html>
                        <html>
                            <body>
                                <h1 style="color:#047BBF; text-align:center;">CONFIRM YOUR NEW EMAIL</h1>
                                <h1 style="text-align:center;">Hey! We received an email change request. It was
                                you?</h1>
                                <h2>Your acess token:<br>{token}</h2>
                                <p>If you didn't request any email change, you should change your password as soon as
                                possible.</p>
                            </body>
                        </html>
                        """, subtype='html')

        try:
            # Gmail -> smtp.gmail.com
            # Hotmail -> smtp.live.com
            # Yahoo -> smtp.mail.yahoo.com
            with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()  # Encrypting our connection to the server
                connection.login(email_sender, email_password)
                connection.send_message(msg)
                return True
        except smtplib.SMTPAuthenticationError as errorMsg:
            print(f"Error: {errorMsg}")
            return False
