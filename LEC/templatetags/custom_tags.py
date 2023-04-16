import re
from typing import Any

from django.forms import Form, BoundField
from django.forms.utils import flatatt
from django.template import Library
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe, SafeString

from accounts.models import LECUser, Notification

register = Library()

@register.simple_tag
def render_field(field, **kwargs):
        return field.as_widget(attrs=kwargs)

@register.filter
def count_unread_notifs(user: LECUser):
    return len(Notification.objects.filter(recipients__pk=user.pk).exclude(read_by__pk=user.pk))
