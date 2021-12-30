import datetime

from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import Student, Advisor
from utils.locale import _


class Course(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(_('course name'), max_length=255)

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    def __str__(self):
        return self.name


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        PENDING = 'P', _('Pending')
        STARTED = 'S', _('Started')
        ENDED = 'E', _('Ended')

    name = models.CharField(_('task name'), max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(_('status'), max_length=1, choices=TaskStatus.choices, default=TaskStatus.PENDING)
    started = models.DateTimeField(_('start time'), null=True, blank=True)
    ended = models.DateTimeField(_('end time'), null=True, blank=True)

    def time_spend(self):
        return self.ended - self.started

    def __str__(self):
        return self.name

    def set_started(self):
        if self.status == Task.TaskStatus.PENDING:
            self.status = Task.TaskStatus.STARTED
            self.started = datetime.datetime.now()
            return True
        return False

    def set_ended(self):
        if self.status == Task.TaskStatus.STARTED:
            self.status = Task.TaskStatus.ENDED
            self.ended = datetime.datetime.now()
            return True
        return False

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
