from allauth.account.adapter import DefaultAccountAdapter
from celery import shared_task


@shared_task
def send_adapter_mail_task(connection, msg):
    connection.send_messages([msg])
