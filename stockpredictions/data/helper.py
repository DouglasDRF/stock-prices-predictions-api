from datetime import datetime, timedelta, date

def get_last_working_day() -> date:
    lastday = datetime.now()
    lastday = lastday - timedelta(days=1)
    if lastday.weekday == "Sunday":
        lastday = lastday - timedelta(days=2)
    elif lastday.weekday == "Saturday":
        lastday = lastday - timedelta(days=1)
    return lastday.date()