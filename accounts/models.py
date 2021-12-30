from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from accounts.managers import UserManager
from utils.locale import _


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    national_code = models.CharField(_('national code'), max_length=10, blank=True, null=True)
    phone_number = models.CharField(_('phone number'), max_length=13, blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    avatar = models.ImageField(_('avatar'), upload_to='avatars', default='avatars/defaults.png')
    age = models.PositiveSmallIntegerField(_('age'), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Advisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(_('Biography'), null=True, blank=True)
    subscription_fee = models.PositiveIntegerField(_('subscription fee'), default=0)

    def __str__(self):
        return self.user.get_full_name()

    @property
    def is_free(self):
        return self.subscription_fee == 0

    class Meta:
        verbose_name = _('advisor')
        verbose_name_plural = _('advisors')


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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField(_('grade'), max_length=4, choices=Grade.choices, default=Grade.UNSET)
    advisor = models.ForeignKey(Advisor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')
