import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

MSG_PLACE_HOLDER = "*msg*"

EMAIL_TAMPLATE =f"""
<h2>Hey BullsAi User,</h2> 
<h2>Your authentication code is:</h2>

<h1>----------------------------</h1>
           <h1>{MSG_PLACE_HOLDER}</h1>
<h1>----------------------------</h1>

<strong><font color="red">DO NOT SHERE THIS CODE WITH ANYONE!</font></strong>

<strong>Have a safe use of BullsAi!</strong>
"""

class MailSender:
    @staticmethod
    def send_email(username: str, password: str, recipient: str, subject: str, body: str) -> None:
        """
        Sends email to the recipient
        Args:
            username (str): the username of the use
            password (str): the password of the user
            recipient (str): email you want to send to 
            subject (str): the subject of the email
            body (str): the body of the email

        Returns:
            None

        example:    
            send_email(my_username, password123, exmp-mail@mail.com, "Hello to John", "Hello John!")
        """
        message = MIMEMultipart()
        message['From'] = username
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body))
        
        try:
            smtp_server = smtplib.SMTP('smtp-relay.sendinblue.com', 587)
            smtp_server.starttls()
            smtp_server.login(username, password)
            smtp_server.sendmail(username, recipient, message.as_string())
            smtp_server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print("Failed to send email. Error: ", e)
