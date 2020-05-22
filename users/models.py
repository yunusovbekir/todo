from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin, UserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class MyUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """ Custom User model """

    username = models.CharField(
        _("Username"),
        max_length=255,
        unique=True,
    )
    email = models.EmailField(
        _('Email Address'),
        max_length=255,
        unique=True,
        db_index=True
    )
    first_name = models.CharField(
        _('First Name'),
        max_length=255,
        blank=True
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=255,
        blank=True
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether '
                    'the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active.'
                    'Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )
    last_login = models.DateTimeField(
        _('last login'),
        default=timezone.now,
    )

    USERNAME_FIELD = 'username'

    objects = MyUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
