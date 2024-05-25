from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_form(sender, message,username):
    message_combined_name = f'the user with username {username} has sent the message {message} '
    send_mail(
        subject='',
        message=message_combined_name,
        from_email=sender,
        recipient_list=['ayoubennaoui20@gmail.com']
    )
