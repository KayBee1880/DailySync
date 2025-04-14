from datetime import datetime, timedelta
from models import HabitLog

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

# Get today's date
today = datetime.today()

# Calculate the Sunday of the current week
days_to_sunday = today.weekday() + 1  
start_of_week = today - timedelta(days=days_to_sunday)
end_of_last_week = start_of_week - timedelta(seconds=1)


def get_week_range():


    # Calculate the Saturday of the current week
    end_of_week = start_of_week + timedelta(days=6)

    # Format both dates as
    start_of_week_str = start_of_week.strftime('%a, %b %d') 
    end_of_week_str = end_of_week.strftime('%a, %b %d')  

    return f"{start_of_week_str} - {end_of_week_str}"

#need a function that will find all timestaps from previous week and all timestamps of current week so far
def get_weekly_logs(habit_id):
    logs_current_week = HabitLog.query.filter(HabitLog.tracked_habit_id == habit_id, HabitLog.date_logged >= start_of_week).count()

    logs_last_week = HabitLog.query.filter(HabitLog.tracked_habit_id == habit_id, HabitLog.date_logged <= end_of_last_week).count()
    return logs_current_week, logs_last_week