from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField


User = get_user_model()


# -----------------------------------------------------------------------------


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

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.cache_deadline = self.deadline

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


# -----------------------------------------------------------------------------


class Contact_Message(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=255,
    )
    email = models.EmailField(
        _('Email'),
        max_length=255,
    )
    subject = models.CharField(
        _('Subject'),
        max_length=255,
    )
    message = models.TextField(
        _('Message'),
    )
    sent_date = models.DateTimeField(
        _('Message sent date'),
        default=timezone.now,
    )
    forwarded_to_email = models.BooleanField(
        _('Message has been forwarded to the email'),
        default=False,
    )

    def __str__(self):
        return "{} - {}".format(self.name, self.subject)

    class Meta:
        verbose_name = _('Message sent by a visitor')
        verbose_name_plural = _('Messages sent by visitors')
        ordering = ('-sent_date',)


# -----------------------------------------------------------------------------


class Menu(models.Model):
    class PositionChoices(models.TextChoices):
        HEADER = 1
        FOOTER = 2
        BOTH = 3
        USEFUL_LINKS = 4

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
        help_text='1 => Header\n 2 => Footer \n 3 => Both \n 4 => Useful Links'
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


# -----------------------------------------------------------------------------


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


# -----------------------------------------------------------------------------


class Website_Settings(models.Model):
    copyright_link = models.URLField(
        _('Link on copyright'),
    )
    about_app_content = RichTextField(
        _('Content on About Application section'),
        blank=True,
    )
    about_me_content = RichTextField(
        _('Content on About me section'),
        blank=True,
    )
    photo = models.ImageField(
        _('Photo'),
        upload_to='settings',
        null=True,
        blank=True,
    )
    full_name = models.CharField(
        _('Full name'),
        max_length=255,
        default='Bakir Yunusov',
    )
    position = models.CharField(
        _('Position'),
        max_length=255,
        default='Python Developer',
    )
    notification_text = models.TextField(
        _("Notification Text"),
        default='You have less 10 minutes left to finish your task.'
    )
    google_map_API_key = models.CharField(
        _('Google Map API Key'),
        max_length=255,
        blank=True
    )
    google_map_location_id = models.CharField(
        _('Google Map Location ID'),
        max_length=255,
        blank=True,
    )

    def __str__(self):
        return "Settings"

    class Meta:
        verbose_name = _('Website Settings')
        verbose_name_plural = _('Website Settings')


# -----------------------------------------------------------------------------


class Social_Accounts(models.Model):
    settings = models.ForeignKey(
        Website_Settings,
        on_delete=models.CASCADE,
    )
    url = models.URLField()
    ordering = models.PositiveIntegerField(
        _("Ordering"),
        default=1,
    )
    a_tag_class = models.CharField(
        _('A tag class name'),
        max_length=255,
        help_text=_('Example: facebook'),
    )
    i_tag_class = models.CharField(
        _('I tag class name'),
        max_length=255,
        help_text=_('Example: bx bxl-facebook'),
    )
    i_tag_class_on_about_me = models.CharField(
        _('I tag class name on About me section'),
        max_length=255,
        help_text=_("Example: icofont-facebook"),
    )
    target_blank = models.BooleanField(
        _('Target blank function'),
        default=False,
        help_text=_('Opens the linked document / page in a new tab')
    )

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = _("Social Account")
        verbose_name_plural = _("Social Accounts")
        ordering = ('ordering',)
