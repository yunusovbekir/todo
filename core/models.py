from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Task(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=False, null=False)
    date_created = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ('date_created',)


class Permitted_User(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    read_only_users = models.ManyToManyField(
        User,
        related_name='read_only_users',
        blank=True,
    )
    comment_allowed_users = models.ManyToManyField(
        User,
        related_name='comment_allowed_users',
        blank=True,
    )

    def __str__(self):
        return self.task.title

    class Meta:
        verbose_name = _('Permitted User')
        verbose_name_plural = _('Permitted Users')


class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.comment_content)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ('comment_date',)
