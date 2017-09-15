from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class EmailUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            ValueError('Email must be specified')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self._create_user(email, password, **kwargs)

    def admins(self):
        return self.filter(is_staff=True, is_superuser=True, is_active=True)

    def inactive_users(self, limit=50):
        return self.filter(is_active=False)[:limit]


class EmailUser(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = EmailUserManager()

    # password = models.CharField(_('password'), max_length=128)
    # last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    is_superuser = models.BooleanField(help_text=_('have all privliges'), default=False)
    email = models.EmailField(help_text=(_('user email')), unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_of_birth = models.DateField(default=timezone.now)

    def clean(self):
        super(EmailUser, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class FailedLoginAttempt(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    user_exists = models.BooleanField(blank=False)
    username = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{} {} {}".format(self.ip, self.username, self.date)
