import hashlib
import random

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.template import TemplateDoesNotExist, engines
from django.template.loader import get_template
from django.utils import six, timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from oscar.apps.customer.managers import CommunicationTypeManager
from oscar.core.compat import AUTH_USER_MODEL
from oscar.models.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(auth_models.BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and
        password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email, is_staff=False, is_active=True,
            is_superuser=False,
            last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(auth_models.AbstractBaseUser,
                   auth_models.PermissionsMixin):

    """
    An abstract base user suitable for use in Oscar projects.

    This is basically a copy of the core AbstractUser model but without a
    username field
    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(
        _('First name'), max_length=255, blank=True)
    last_name = models.CharField(
        _('Last name'), max_length=255, blank=True)
    is_staff = models.BooleanField(
        _('Staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'),
                                       default=timezone.now)
    phone_number = PhoneNumberField(_("Phone number"), blank=True, default="1390000000")
    date_birth = models.DateTimeField(_('Birthday'), default=timezone.now)

    MALE, FEMALE = 'M', 'F'
    choices = (
        (MALE, 'Male'),
        (FEMALE, 'Female'))
    gender = models.CharField(max_length=1, choices=choices,
                              verbose_name='Gender',default='M')
    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def _migrate_alerts_to_user(self):
        """
        Transfer any active alerts linked to a user's email address to the
        newly registered user.
        """
        ProductAlert = self.alerts.model
        alerts = ProductAlert.objects.filter(
            email=self.email, status=ProductAlert.ACTIVE)
        alerts.update(user=self, key='', email='')

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        # Migrate any "anonymous" product alerts to the registered user
        # Ideally, this would be done via a post-save signal. But we can't
        # use get_user_model to wire up signals to custom user models
        # see Oscar ticket #1127, Django ticket #19218
        self._migrate_alerts_to_user()


from oscar.apps.customer.models import *