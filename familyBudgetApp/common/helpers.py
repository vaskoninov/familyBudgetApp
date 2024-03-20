from django.utils import timezone


def get_current_year():
    return timezone.now().year


def get_current_month():
    return timezone.now().month


def get_previous_month_and_year(month, year):
    previous_month = month - 1 if month != 1 else 12
    previous_year = year if month != 1 else year - 1
    return previous_month, previous_year
