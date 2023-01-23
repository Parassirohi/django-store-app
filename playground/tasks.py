
from time import sleep
from celery import shared_task


@shared_task()
def notify_customers(messages):
    print('Sending 10k emails...')
    print(messages)
    sleep(10)
    print('Emails were successfully sent!')

