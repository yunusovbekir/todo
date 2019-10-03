from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse

class Task(models.Model):
    title = models.CharField(max_length = 100)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    description = models.CharField(max_length = 300, blank=False, null=False)
    date_created = models.DateTimeField(default = timezone.now)
    deadline = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk':self.pk})


class Permitted_Users(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, to_field='id')
    permitted_username = models.ForeignKey(User, on_delete = models.CASCADE)
    can_comment = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.permitted_username)

    def get_absolute_url(self):
        return reverse('permitted-users', kwargs={'pk':self.pk})

class Comment(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return "{}".format(self.comment_content)
