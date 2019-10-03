import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery.task.schedules import crontab
from django.core.mail import EmailMessage
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import datetime

from .models import *

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name='sending_emails'
    )
def sending_emails():
    tasks = Task.objects.all()                          #get all tasks
    ex_tasks = []                                       #stored ex-tasks
    now = datetime.datetime.now()

    for task in tasks:
        deadline = task.deadline                        #get deadline of task
        user = task.author                              #get author of task
        if deadline <= now + datetime.timedelta(minutes=10) and not task in ex_tasks:   #if deadline is less than 10 min and not a task that already has received a reminder
            receiver_user = User.objects.get(username=user) #access User model
            email = receiver_user.email                     #get email of author
            ex_tasks.append(task)                           #store in order to prevent sending email again
        return email


    Subject = 'Kind Reminder'
    Message =  'You have left 10 minutes to finish your task!'
    email_send = EmailMessage(Subject, Message, to=[email])
    logger.info("Email sent to {0}".format(email))
    return email_send.send()
