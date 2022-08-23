import smtplib
from email.message import EmailMessage


class Email:
    def __repr__(self) -> str:
        return f'{self.__class__.__name__} Class'

    @staticmethod
    def send_email(receiver: str, token: str) -> bool:
        """Send an email with the authentication token"""
        email_sender = 'your_email_here@gmail.com'  # Your Google account here
        email_password = 'you_app_password_here'  # Your app password here
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
