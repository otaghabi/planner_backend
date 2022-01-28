from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from accounts.managers import UserManager
from utils.locale import _


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), unique=True)
    first_name = models.CharField(_('First Name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)
    national_code = models.CharField(_('National Code'), max_length=10, blank=True, null=True)
    phone_number = models.CharField(_('Phone Number'), max_length=13, blank=True, null=True)
    avatar = models.ImageField(_('Avatar'), upload_to='avatars', blank=True, null=True)
    age = models.PositiveSmallIntegerField(_('Age'), blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff'), default=False)
    is_superuser = models.BooleanField(_('Super User'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Advisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    bio = models.TextField(_('Biography'), null=True, blank=True)
    subscription_fee = models.PositiveIntegerField(_('Subscription fee'), default=0)

    def __str__(self):
        return self.user.get_full_name()

    @property
    def is_free(self):
        return self.subscription_fee == 0

    class Meta:
        verbose_name = _('Advisor')
        verbose_name_plural = _('Advisors')


class Student(models.Model):
    class Grade(models.TextChoices):
        ONE = '1', _('One')
        TWO = '2', _('Two')
        THREE = '3', _('Three')
        FOUR = '4', _('Four')
        FIVE = '5', _('Five')
        SIX = '6', _('Six')
        SEVEN = '7', _('Seven')
        EIGHT = '8', _('Eight')
        NINE = '9', _('Nine')
        TEEN = '10', _('Teen')
        ELEVEN = '11', _('Eleven')
        TWELVE = '12', _('Twelve')
        BACHELOR = 'BC', _('Bachelor')
        MASTERS = 'MA', _('Masters')
        PHD = 'PHD', _('Phd')
        UNSET = 'NONE', _('Unset')

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    grade = models.CharField(_('grade'), max_length=4, choices=Grade.choices, default=Grade.UNSET)
    advisor = models.ForeignKey(Advisor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Advisor'))

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
