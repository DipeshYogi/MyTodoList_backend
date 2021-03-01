from celery import shared_task
from django.core.management import call_command

@shared_task
def sample_task():
    print("The sample task just ran successfully!!!!!!!!!!!!!!")


@shared_task
def send_email_reminder():
    call_command('send_reminder')

    