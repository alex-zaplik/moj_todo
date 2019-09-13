import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class NamedModel(models.Model):
    """
    A model that has a name that is used to represent it (in __str__)
    """

    class Meta:
        abstract = True

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Table(NamedModel):
    """
    A todo table that contains columns used for organising task.
    Each table has it's own name (doesn't have to be unique) and
    a list of users that can access it.
    """

    users = models.ManyToManyField(User)


class Column(NamedModel):
    """
    Each column belongs to a single table and has a name that doen't
    have to be unique. It is a container for tasks.
    """

    table = models.ForeignKey(Table, on_delete=models.CASCADE)


class Task(NamedModel):
    """
    A single task describes what has to be done via a name,
    a description and a deadline. More fields will probably be
    added in the future
    """

    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    done = models.BooleanField(default=False)

    def is_near_to_deadline(self):
        """
        If a task's deadline is less than a day away it is considered
        near to it. This flag can be used to stress that fact on the
        website.
        """

        now = timezone.now()
        near = now + datetime.timedelta(days=1) >= self.deadline
        return near and not self.done
