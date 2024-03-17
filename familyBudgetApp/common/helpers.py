from django.utils import timezone


def current_year():
    return timezone.now().year


def current_month():
    return timezone.now().month


def get_previous_month_and_year(current_month, current_year):
    previous_month = current_month - 1 if current_month != 1 else 12
    previous_year = current_year if current_month != 1 else current_year - 1
    return previous_month, previous_year
