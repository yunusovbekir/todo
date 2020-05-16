from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Permitted_User


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
