from django.db import models
from django.contrib.auth.models import User

from datetime import timedelta

class Employee(User):
    start_date = models.DateField()

class Leave(models.Model):
    STATUSES = (
            ("new", "new"),
            ("approved", "approved"),
            ("declined", "declined"),
        )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.TextField(max_length=8, choices = STATUSES)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def _days_of_leave(self):
        date_counter = self.start_date
        days_of_week_counter = 0
        while date_counter <= self.end_date:
            # 0 is Monday, 6 is Sunday
            if date_counter.weekday() < 5:
                days_of_week_counter += 1
            date_counter += timedelta(days=1)
        return days_of_week_counter
    days_of_leave = property(_days_of_leave)

