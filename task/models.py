from django.db import models
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class Task(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=100,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Author'),
    )
    description = RichTextField(
        _("Description"),
        max_length=300,
        blank=False,
        null=False,
    )
    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now
    )
    deadline = models.DateTimeField(
        _("Deadline"),
        default=timezone.now,
    )

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.cache_deadline = self.deadline

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

    def get_permitted_user_object(self):
        return self.permitted_user_set.first()

    @property
    def comment_allowed_users(self):
        permitted_user_object = self.get_permitted_user_object()
        return permitted_user_object.comment_allowed_users.all()

    @property
    def read_only_users(self):
        permitted_user_object = self.get_permitted_user_object()
        return permitted_user_object.read_only_users.all()

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ('date_created',)


# -----------------------------------------------------------------------------


class Permitted_User(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_('Task'),
    )
    read_only_users = models.ManyToManyField(
        User,
        related_name='read_only_users',
        blank=True,
        verbose_name=_("Read-only users"),
    )
    comment_allowed_users = models.ManyToManyField(
        User,
        related_name='comment_allowed_users',
        blank=True,
        verbose_name=_("Comment-allowed users"),
    )

    def __str__(self):
        return self.task.title

    class Meta:
        verbose_name = _('Permitted User')
        verbose_name_plural = _('Permitted Users')


# -----------------------------------------------------------------------------


class Comment(models.Model):
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Username"),

    )
    comment_content = models.TextField(
        _('Comment content'),
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_("Task"),
    )
    comment_date = models.DateTimeField(
        _('Comment date'),
        default=timezone.now,
    )

    def __str__(self):
        return "{}".format(self.comment_content)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ('comment_date',)
