from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from celery import shared_task


@shared_task(autoretry_for=(Exception,), max_retries=5)
def notify(subject, msg, from_email, to_email):
    return send_mail(
        subject,
        msg,
        from_email,
        [to_email],
        fail_silently=False,
    )
