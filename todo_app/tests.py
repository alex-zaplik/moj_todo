import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Table, Column, Task

class TaskModelTests(TestCase):
    def test_near_deadline_past_task(self):
        """
        Tasks with a deadline in the past are considered near
        their deadline only if they are not flagged as done.
        """

        time = timezone.now() + datetime.timedelta(days=-5)
        done = Task(deadline=time, done=True)
        not_done = Task(deadline=time, done=False)

        self.assertIs(done.is_near_to_deadline(), False)
        self.assertIs(not_done.is_near_to_deadline(), True)
    

    def test_near_deadline_future_task(self):
        """
        Tasks with a deadline further than a day into the furute
        are not considered near their deadline no matter if they
        are done or not.
        """

        time = timezone.now() + datetime.timedelta(days=5)
        done = Task(deadline=time, done=True)
        not_done = Task(deadline=time, done=False)

        self.assertIs(done.is_near_to_deadline(), False)
        self.assertIs(not_done.is_near_to_deadline(), False)
    

    def test_near_deadline_near_task(self):
        """
        Tasks with a deadline less than a day into the furute
        are considered near their deadline only if they are
        not flagged as done.
        """

        time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        done = Task(deadline=time, done=True)
        not_done = Task(deadline=time, done=False)

        self.assertIs(done.is_near_to_deadline(), False)
        self.assertIs(not_done.is_near_to_deadline(), True)
