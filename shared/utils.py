import threading

from decouple import config
from django.core.mail import send_mail
from twilio.rest import Client

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

        verification_check = client.verify \
            .v2 \
            .services('VA9060063ba3efe707a8ca8e9c37f29e9d') \
            .verification_checks \
            .create(to='+998900355948', code='[Code]')

        print(verification_check.status)

    thread = threading.Thread(target=send_in_thread)
    thread.start()

    return True
