import threading
from django.core.mail import send_mail
from django.conf import settings

def send_email_async(subject, message, recipient_list):
    def _send():
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
    threading.Thread(target=_send).start()
