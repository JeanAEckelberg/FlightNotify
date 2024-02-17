"""
Email utilities file
"""

import smtplib
from email.message import EmailMessage


def generate_email(email_text: str, email_address: str) -> EmailMessage:
    """
    Create an email
    :param email_text: content of the email
    :param email_address: address to send and receive the notification
    :return: Email message
    """
    msg: EmailMessage = EmailMessage()
    msg['From'] = email_address
    msg['To'] = email_address
    msg['Subject'] = 'Flight Notify'
    msg.set_content(email_text)
    return msg


def send_email(email_text: str, email_address: str, email_password: str) -> None:
    """
    Send an email via gmail smtp
    :param email_text: content of the email
    :param email_address: address to send and receive the notification
    :param email_password: app password to log in
    :return: None
    """
    msg: EmailMessage = generate_email(email_text, email_address)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(email_address, email_password)
        smtp_server.sendmail(email_address, email_address, msg.as_string())
    print("Message sent!")
