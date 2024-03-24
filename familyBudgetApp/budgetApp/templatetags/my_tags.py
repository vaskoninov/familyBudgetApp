import calendar

from django import template
from django.contrib.auth import get_user_model

from familyBudgetApp.budgetApp.models import BudgetItem
from familyBudgetApp.common.models import Tag

UserModel = get_user_model()
register = template.Library()


@register.filter
def month_name(month_number):
    month_number = int(month_number)
    return calendar.month_name[month_number]


@register.inclusion_tag("templatetags/tags.html")
def tags_available():
    tags = Tag.objects.all()
    return {"tags": tags}


@register.inclusion_tag("templatetags/last-five.html", takes_context=True)
def last_five(context, item_type, url_name):
    month = context['month']
    year = context['year']
    user = context['request'].user

    last_five_budget_items = BudgetItem.objects.filter(date__month=month, date__year=year, user=user,
                                                       item_type=item_type).order_by("-date")[:5]

    return {"last_five": last_five_budget_items, "url_name": url_name}


@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})