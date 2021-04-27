from datetime import datetime, timedelta


# TODO: please rewrite
def youtube_date_format(date_input: datetime) -> str:
    diff = datetime.utcnow() - date_input

    if diff <= timedelta(seconds=1):
        return "Now"
    elif diff <= timedelta(minutes=1):
        date = diff.total_seconds()
        mode = "seconds" if date > 1 else "second"
    elif diff <= timedelta(hours=1):
        date = diff.total_seconds() // 60
        mode = "minutes" if date > 1 else "minute"
    elif diff <= timedelta(days=1):
        date = diff.total_seconds() // 60 // 60
        mode = "hours" if date > 1 else "hour"
    elif diff <= timedelta(days=30):
        date = diff.days
        mode = "days" if date > 1 else "day"
    elif diff <= timedelta(days=30 * 12):
        date = diff.days // 30
        mode = "months" if date > 1 else "month"
    else:
        date = diff.seconds // 60 // 60 // 24 // 30 // 12
        mode = "years" if date > 1 else "year"

    # print(f"{date} {mode} ago")
    # print(diff)
    return f"{date} {mode} ago"
