from celery.task.schedules import crontab
from django.core.mail import EmailMessage
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import datetime
from django.contrib.auth import get_user_model
from .models import Task


User = get_user_model()
logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name='sending_emails'
)
def sending_emails():
    tasks = Task.objects.all()  # get all tasks
    ex_tasks = []  # stored ex-tasks
    now = datetime.datetime.now()

    for task in tasks:
        deadline = task.deadline  # get deadline of task
        user = task.author  # get author of task

        # if deadline is less than 10 min and
        # not a task that already has received a reminder
        if deadline <= now + datetime.timedelta(minutes=10) \
                and task not in ex_tasks:
            # access User model
            receiver_user = User.objects.get(username=user)

            # get email of author
            email = receiver_user.email

            # store in order to prevent sending email again
            ex_tasks.append(task)
        return email

    Subject = 'Kind Reminder'
    Message = 'You have left 10 minutes to finish your task!'
    email_send = EmailMessage(Subject, Message, to=[email])
    logger.info("Email sent to {0}".format(email))
    return email_send.send()
