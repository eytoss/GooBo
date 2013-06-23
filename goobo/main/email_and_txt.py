"""
hint.py - Hint Module
"""
from django.conf import settings


def send_email(reply_to, message):
    """send email functionality"""
    _send_email_or_txt(reply_to, message, is_txt=0)


def send_txt(reply_to, message):
    """send txt functionality"""
    _send_email_or_txt(reply_to, message, is_txt=1)


def _send_email_or_txt(reply_to, message, is_txt=1):
    """send_email functionality"""
    # Import smtplib for the actual sending function
    import smtplib
    # Import the email modules we'll need
    from email.mime.text import MIMEText
    # Create a text/plain message
    msg = MIMEText(message)

    destination = settings.EMAIL_TO
    if is_txt:
        destination = settings.EMAIL_TO_TXT_GATEWAY
    msg['Subject'] = 'Message from {}'.format(reply_to)
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = destination

    s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    # this is needed if you want to do login authentication with gmail
    s.starttls()
    s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    s.sendmail(settings.EMAIL_FROM, [destination], msg.as_string())
    s.quit()
