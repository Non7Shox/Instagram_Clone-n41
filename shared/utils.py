import threading

from django.core.mail import send_mail
from twilio.rest import Client
from decouple import config


from config.settings import EMAIL_HOST


def send_code_to_email(email, code):
    def send_in_thread():
        send_mail(
            from_email=EMAIL_HOST,
            recipient_list=[email],
            subject="Activation code",
            message=f"Your activation code is {code}"
        )

    thread = threading.Thread(target=send_in_thread)
    thread.start()

    return True


def send_code_to_phone(phone_number, code):
    def send_in_thread():
        account_sid = config('TWILIO_ID')
        auth_token = config('TWILIO_KEY')
        client = Client(account_sid, auth_token)

        client.messages.create(
            from_='+14157992530',
            to='+998335900441',
            body=f"Your activation code is {code}"
        )

    thread = threading.Thread(target=send_in_thread)
    thread.start()

    return True
