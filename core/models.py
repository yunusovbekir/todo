from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField


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


class Menu(models.Model):
    class PositionChoices(models.TextChoices):
        HEADER = _("Header")
        FOOTER = _("Footer")
        BOTH = _("Both")
        USEFUL_LINKS = _("Useful Links")

    title = models.CharField(
        _('Title'),
        max_length=255,
    )
    url = models.CharField(
        _('Url'),
        max_length=50,
        help_text=_("Example /about/ -page url"),
    )
    position = models.CharField(
        _('Position'),
        max_length=50,
        choices=PositionChoices.choices,
    )
    ordering = models.PositiveIntegerField(
        _('Ordering'),
        default=1,
    )
    target_blank = models.BooleanField(
        _('Target blank function'),
        default=False,
        help_text=_('Opens the linked document / page in a new tab')
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')
        ordering = ('ordering',)


class Contact(models.Model):

    class ContactType(models.TextChoices):
        ADDRESS = _('Address')
        EMAIL = _('Email')
        PHONE = _('Phone')

    type = models.CharField(
        _('Contact type'),
        max_length=50,
        choices=ContactType.choices,
    )
    content = RichTextField(
        _('Content'),
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
