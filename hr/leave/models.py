from django.db import models
from django.contrib.auth.models import User

from datetime import date
from dateutil.relativedelta import relativedelta

class Employee(User):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key = True,
    )
    start_date = models.DateField()

    def _leave_remaining(self):
        """
        Return amount of leave remaining in the current period
        """
        periods = self.get_periods(self.start_date, date.today())
        days_remaining = 18
        for period in periods:
            days_remaining -= self.leave_taken(period[0], period[1])
            if days_remaining > 5:
                days_remaining = 23
            else:
                days_remaining+= 18
        return days_remaining
    leave_remaining = property(_leave_remaining)


    def get_periods(self, start_date, end_date):
        """
        Return a list of 12 month working periods within a start and end date

        Each returned period in the list is a tuple and consists of 2 values :
        the start date and end date of the period respectively


        """
        if relativedelta(end_date, start_date).years <= 1:
            return [(start_date, end_date)]
        elif relativedelta(end_date, start_date).years > 1:
            end_of_period = start_date + relativedelta(years=+1, days=-1)
            periods = [(start_date, end_of_period)]
            while relativedelta(end_date, end_of_period).years >= 1:
                start_of_period = end_of_period + relativedelta(days=1)
                end_of_period += relativedelta(years= +1, days= -1)
                periods.append((start_of_period,end_of_period))
            periods.append((end_of_period + relativedelta(days=1),end_date))
            return periods
        else:
            raise ValueError("""start_date must be before end_date and both
            must be datetime objects""")

    def leave_taken(self, start_date, end_date):
        """
        Return the number of days of leave taken between the supplied dates

        """
        leave_list = Leave.objects.filter(
           start_date__gte = start_date,
           end_date__lte = end_date
           )
        days_taken = 0
        for leave_object in leave_list:
            # This is a naive solution that assumes that leave dates will not
            # cross working period boundaries. For simplicity we just use the
            # Leave model's days_taken property
            if leave_object.status == 'approved':
                days_taken += leave_object.working_days_in_leave_period
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

    def _working_days_in_leave_period(self):
        date_counter = self.start_date
        days_of_week_counter = 0
        while date_counter <= self.end_date:
            # 0 is Monday, 6 is Sunday
            if date_counter.weekday() < 5:
                days_of_week_counter += 1
            date_counter += relativedelta(days=1)
        return days_of_week_counter
    working_days_in_leave_period = property(_working_days_in_leave_period)
