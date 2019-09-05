import uuid
from collections import OrderedDict

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from users.utils import date_expired_default
from users.mixins import NoDeleteModelMixin


# Create your models here.

# 用户组
class UserGroup(NoDeleteModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True, verbose_name=_('Name'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    date_created = models.DateTimeField(auto_now_add=True, null=True,
                                        verbose_name=_('Date created'))
    created_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("User group")

    @classmethod
    def initial(cls):
        default_group = cls.objects.filter(name='Default')
        if not default_group:
            group = cls(name='Default', created_by='System', comment='Default user group')
            group.save()
        else:
            group = default_group[0]
        return group


# 用户，继承Django内部用户类
class User(AbstractUser):
    ROLE_ADMIN = 'Admin'
    ROLE_USER = 'User'

    ROLE_CHOICES = (
        (ROLE_ADMIN, _('Administrator')),
        (ROLE_USER, _('User'))
    )
    OTP_LEVEL_CHOICES = (
        (0, _('Disable')),
        (1, _('Enable')),
        (2, _("Force enable")),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    username = models.CharField(
        max_length=128, unique=True, verbose_name=_('Username')
    )
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    email = models.EmailField(
        max_length=128, unique=True, verbose_name=_('Email')
    )
    groups = models.ManyToManyField(
        'users.UserGroup', related_name='users',
        blank=True, verbose_name=_('User group')
    )
    role = models.CharField(
        choices=ROLE_CHOICES, default='User', max_length=36,
        blank=True, verbose_name=_('Role')
    )
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_('Phone')
    )
    otp_level = models.SmallIntegerField(
        default=0, choices=OTP_LEVEL_CHOICES, verbose_name=_('MFA')
    )

    date_expired = models.DateTimeField(
        default=date_expired_default, blank=True, null=True,
        verbose_name=_('Date expired')
    )

    comment = models.TextField(
        max_length=200, blank=True, verbose_name=_('Comment')
    )

    def __str__(self):
        return '{0.name}({0.username})'.format(self)

    @property
    def password_raw(self):
        raise AttributeError('Password raw is not a readable attribute')

    @password_raw.setter
    def password_raw(self, password_raw_):
        self.set_password(password_raw_)

    @property
    def is_expired(self):
        if self.date_expired and self.date_expired < timezone.now():
            return True
        else:
            return False

    @property
    def is_valid(self):
        if self.is_active and not self.is_expired:
            return True
        return False

    @property
    def is_superuser(self):
        if self.role == 'Admin':
            return True
        else:
            return False

    @is_superuser.setter
    def is_superuser(self, value):
        if value is True:
            self.role = 'Admin'
        else:
            self.role = 'User'

    @property
    def is_staff(self):
        if self.is_authenticated and self.is_valid:
            return True
        else:
            return False

    @is_staff.setter
    def is_staff(self, value):
        pass

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.username
        if self.username == 'admin':
            self.role = 'Admin'
            self.is_active = True

        super().save(*args, **kwargs)

    @property
    def otp_enabled(self):
        return self.otp_level > 0

    @property
    def otp_force_enabled(self):
        return self.otp_level == 2

    def enable_otp(self):
        if not self.otp_force_enabled:
            self.otp_level = 1

    def force_enable_otp(self):
        self.otp_level = 2

    def disable_otp(self):
        self.otp_level = 0
        self.otp_secret_key = None

    def to_json(self):
        return OrderedDict({
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser,
            'opt_role': self.get_role_display(),
            'role': self.get_role_display(),
            'groups': [group.name for group in self.groups.all()],
            'phone': self.phone,
            'otp_level': self.otp_level,
            'comment': self.comment,
            'date_expired': self.date_expired.strftime('%Y-%m-%d %H:%M:%S') if self.date_expired is not None else None
        })

    def reset_password(self, new_password):
        self.set_password(new_password)
        self.save()

    def delete(self, using=None, keep_parents=False):
        if self.pk == 1 or self.username == 'admin':
            return
        return super(User, self).delete()

    class Meta:
        ordering = ['username']
        verbose_name = _("User")

    @classmethod
    def initial(cls):
        user = cls(username='admin',
                   email='admin@itnotebooks.com',
                   name=_('Administrator'),
                   first_name=_('Super'),
                   last_name=_('Manager'),
                   password_raw='admin',
                   role='Admin',
                   comment=_('Administrator is the super user of system')
                   )
        user.save()
        user.groups.add(UserGroup.initial())
