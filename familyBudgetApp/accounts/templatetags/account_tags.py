from django import template
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

register = template.Library()
UserModel = get_user_model()


@register.filter(name='has_group')
def has_group(user, group_name):
    if not user or not hasattr(user, 'groups'):
        return False
    try:
        return user.groups.filter(name=group_name).exists()
    except Group.DoesNotExist:
        return False
