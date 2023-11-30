from celery import shared_task
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_adapter_mail_task(serialized_msg):
    extra_headers = serialized_msg.pop('extra_headers')
    msg = EmailMultiAlternatives(**serialized_msg)
    msg.extra_headers = extra_headers
    msg.send()
