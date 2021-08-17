import  smtplib
from django.conf import settings


def send_email():
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOTS,settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print('Conectado...')
    except Exception as e:
        print(e)