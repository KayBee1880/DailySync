from datetime import datetime, timedelta
import calendar
from models import HabitLog
import pytz

def validate_password(password1, password2):
    if password1 == password2:
        pass
    else:
        return (False, "Passwords do not match", "error")
    
    if len(password1)  < 6:
        return (False,"Password must be at least 6 characters long",'warning')
    elif not any(letter.isupper() for letter in password1):
        return (False,"Password must have at least 1 uppercase character",'warning')
    elif not any(char in '~!@#$%^&*(),.?' for char in password1):
        return (False,"Password must have at least 1 valid special character",'warning')
    return (True,None,'success')     


def get_local_today(timezone_str="America/Chicago"):
    tz = pytz.timezone(timezone_str)
    return datetime.now(tz).date()
    


# Calculate the Sunday of the current week
def get_current_week_dates(week_offset=0):
    today = datetime.today() + timedelta(weeks=week_offset)
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)
    return [start_of_week + timedelta(days=i) for i in range(7)]

def get_week_range(week_offset = 0):
    today = datetime.today() + timedelta(weeks=week_offset)
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)
    end_of_week = start_of_week + timedelta(days=6)

    start_of_week_str = start_of_week.strftime('%a, %b %d') 
    end_of_week_str = end_of_week.strftime('%a, %b %d')  

    return f"{start_of_week_str} - {end_of_week_str}"

#need a function that will find all timestaps from previous week and all timestamps of current week so far
def get_weekly_logs():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)
    end_of_week = start_of_week + timedelta(days=6)
    end_of_last_week = start_of_week - timedelta(days=1)
    start_of_last_week = end_of_last_week - timedelta(days=6)

    current_week, last_week = (start_of_week.date(),end_of_week.date()), (start_of_last_week.date(), end_of_last_week.date())
    return current_week, last_week  

def get_monthly_logs():
    today = datetime.today()

    # This month range
    start_of_this_month = today.replace(day=1)
    last_day_this_month = calendar.monthrange(today.year, today.month)[1]
    end_of_this_month = today.replace(day=last_day_this_month)

    # Last month range
    if today.month == 1:
        start_of_last_month = today.replace(year=today.year - 1, month=12, day=1)
    else:
        start_of_last_month = today.replace(month=today.month - 1, day=1)

    last_day_last_month = calendar.monthrange(start_of_last_month.year, start_of_last_month.month)[1]
    end_of_last_month = start_of_last_month.replace(day=last_day_last_month)

    this_month = (start_of_this_month.date(), end_of_this_month.date())
    last_month = (start_of_last_month.date(), end_of_last_month.date())

    return this_month, last_month
