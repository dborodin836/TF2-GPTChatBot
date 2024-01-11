import datetime


def get_date(epoch: int, relative_epoch_time: int = None) -> str:
    account_created_date = datetime.date.fromtimestamp(epoch)

    if relative_epoch_time is not None:
        current_date = datetime.date.fromtimestamp(relative_epoch_time)
    else:
        current_date = datetime.date.today()

    age_months = (
        current_date.month
        - account_created_date.month
        - (current_date.day < account_created_date.day)
    )
    if age_months < 0:
        age_months += 12
    age_days = (current_date - account_created_date.replace(year=current_date.year)).days
    # Get the age tuple in years, months, and days
    age = datetime.timedelta(days=age_days)
    age_years, remainder_days = divmod(age.days, 365)
    age_months, remainder_days = divmod(remainder_days, 30)
    age_days = remainder_days
    age_years = (
        current_date.year
        - account_created_date.year
        - (
            (current_date.month, current_date.day)
            < (account_created_date.month, account_created_date.day)
        )
    )
    return f"{age_years} years {age_months} months {age_days} days"
