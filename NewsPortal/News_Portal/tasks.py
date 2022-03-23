from celery import shared_task
import time

@shared_task
def printer():
    time.sleep(10)
    print('pewpew')