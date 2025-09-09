from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name):
    """Функция для определения группы прав на сервере."""

    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
