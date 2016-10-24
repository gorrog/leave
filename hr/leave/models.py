from django.db import models
from django.contrib.auth.models import User

from datetime import timedelta, date

class Employee(User):
    start_date = models.DateField()

    def _leave_remaining(self):
        periods = self.get_periods(self.start_date, date.today())
        days_remaining = 18
        for period in periods:
            days_remaining -= self.leave_taken(period)
            if days_remaining > 5:
                days_remaining = 23
            else:
                days_remaining+= 18
        return days_remaining
    leave_remaining = property(_leave_remaining)


    def get_periods(self, start_date, end_date):
        if end_date - start_date <= timedelta(years=1):
            return [(start_date, end_date)]
        elif end_date - start_date > timedelta(years=1):
            end_of_period = start_date + timedelta(days=364)
            periods = [(start_date, end_of_period)]
            while (end_date - end_of_period) >= timedelta(years=1):
                start_of_period = end_of_period + timedelta(days=1)
                end_of_period += timedelta(days=364)
                periods.append((start_of_period,end_of_period))
            periods.append((end_of_period + timedelta(days=1),end_date))
            return periods
        else:
            raise ValueError("""start_date must be before end_date and both
            must be datetime objects""")

    def leave_taken(self, start_date, end_date):
        leave_list = Leave.objects.filter(
           start_date__gte = start_date,
           end_date__lte = end_date
           )
        days_taken = 0
        for leave_object in leave_list:
            # This is a naive solution that assumes that leave dates will not
            # cross working anniversaries. For simplicity we just use the Leave
            # model's days_taken property
            days_taken += leave_object.days_of_leave
        return days_taken


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
