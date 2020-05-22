from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .models import Task, Permitted_User, Website_Settings
from .tasks import notify


@receiver(post_save, sender=Task,
          dispatch_uid='create_permitted_user_model')
def create_permitted_user_model(sender, created, **kwargs):
    """
    As soon as a new Task object is created,
     create the related Permitted User objects
    """

    instance = kwargs.get('instance')
    if created:
        Permitted_User.objects.create(task=instance)


@receiver(pre_save, sender=Task, dispatch_uid='send_notification')
def send_notification(sender, **kwargs):
    instance = kwargs.get('instance')

    if instance.deadline != instance.cache_deadline:
        instance.cache_deadline = instance.deadline
        settings = Website_Settings.objects.first()
        text_on_time = settings.notification_text_on_time
        text_less_ten_minutes = settings.notification_text_less_ten_min

        # get difference between deadline and current datetime
        delta = instance.deadline - timezone.now()

        # notification must be sent 10 minutes before the time is over
        countdown = delta.total_seconds() - (60 * 10)

        from_email = 'yunusovbekir@gmail.com'
        to_email = instance.author.email
        subject = _('Task notification - {}'.format(instance.title))
        if countdown:
            msg = _('{}\n'
                    'Task details:\n'
                    'Title: {}\n'
                    'Description: {}\n'
                    'Deadline: {}\n'.
                    format(text_on_time,
                           instance.title,
                           instance.description,
                           instance.deadline)
                    )

            notify.apply_async(
                (subject, msg, from_email, to_email),
                countdown=countdown
            )
