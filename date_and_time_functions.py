from datetime import datetime

def merge_into_DateTime(date_var, time_var):
    """take a date_time object and extract the date and a time object from a form and add the time to the date to make a new, complete date_time object that can be passed into sqlalchemy"""

    merged_datetime = datetime.datetime.combine(date_var,time_var)
    #remove timezone info (do on client-side)
    merged_datetime = merged_datetime.replace(tzinfo=None)

    return merged_datetime

def get_now_for_sqlalchemy():
    now = now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time
