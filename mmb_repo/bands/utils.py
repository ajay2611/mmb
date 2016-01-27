__author__ = 'ajaysingh'

from django.core.mail import send_mail
from django.core import mail


def send_multiple_mails(sub, msg, fro, to_list):
    connection = mail.get_connection()
    connection.open()
    for to in to_list:
        try:
            print 'sending mail to - ', to
            email = mail.EmailMessage(sub, msg, 'noreply@makemyband.in', [to], connection=connection)
            email.send()
        except Exception as e:
            print str(e)

    connection.close()