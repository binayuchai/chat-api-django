from django.core.mail import EmailMessage
import os
from decouple import config


class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=config('EMAIL_HOST_FROM'),
            to = [data['to_email']]
        )
        email.send()