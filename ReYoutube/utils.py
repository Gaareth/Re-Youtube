from datetime import datetime, timedelta


#TODO: please rewrite
def youtube_date_format(date_input: datetime) -> str:
    diff = datetime.now() - date_input

    if diff <= timedelta(minutes=1):
        return "Now"
    elif diff <= timedelta(hours=1):
        date = diff.seconds // 60
        mode = "minutes" if date > 1 else "minute"
    elif diff <= timedelta(hours=24):
        date = diff.seconds // 60 // 60
        mode = "hours" if date > 1 else "hour"
    elif diff <= timedelta(days=30):
        date = diff.seconds // 60 // 60 // 24
        mode = "days" if date > 1 else "day"
    elif diff <= timedelta(days=30 * 12):
        date = diff.seconds // 60 // 60 // 24 // 30
        mode = "months" if date > 1 else "month"
    else:
        date = diff.seconds // 60 // 60 // 24 // 30 // 12
        mode = "years" if date > 1 else "year"
    return f"{date} {mode} ago"
