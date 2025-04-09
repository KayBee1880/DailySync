from datetime import datetime, timedelta

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


def get_week_range():
    # Get today's date
    today = datetime.today()

    # Calculate the Sunday of the current week
    days_to_sunday = today.weekday() + 1  
    start_of_week = today - timedelta(days=days_to_sunday)

    # Calculate the Saturday of the current week
    end_of_week = start_of_week + timedelta(days=6)

    # Format both dates as
    start_of_week_str = start_of_week.strftime('%a, %b %d') 
    end_of_week_str = end_of_week.strftime('%a, %b %d')  

    return f"{start_of_week_str} - {end_of_week_str}"