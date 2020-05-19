from math import trunc

from django import template
from django.utils import timezone


register = template.Library()


@register.filter
def get_datetime_difference_for_comment(value):
    """
    Calculate difference between input datetime value and current datetime
    """

    delta = timezone.now() - value
    hours = delta.total_seconds() / (60 * 60)
    minutes = delta.total_seconds() / 60

    hours = trunc(hours)
    minutes = trunc(minutes)

    if hours < 1:
        if minutes == 0:
            minutes = 1
        return '{}m'.format(minutes)
    elif hours > 24:
        days = round(hours / 24)
        return '{}d'.format(days)
    return '{}h'.format(hours)


@register.filter
def get_datetime_difference_for_deadline(value):
    """
    Calculate difference between input datetime value and current datetime
    """

    delta = value - timezone.now()
    if delta.total_seconds() < 0:
        return 'Expired'
    else:

        # get difference
        days = delta.total_seconds() / (60 * 60 * 24)
        hours = delta.total_seconds() / (60 * 60)
        minutes = delta.total_seconds() / 60

        # calculate days, hours and minutes
        days = trunc(days)
        hours = trunc(hours - (days * 24))
        minutes = trunc(minutes - (days * 24 * 60) - (hours * 60))

        if days == 0 and hours == 0 and minutes == 0:
            return 'Less than a minute left.'
        elif days == 0 and hours == 0:
            return '{} minute(s) left.'.format(minutes)
        elif days == 0:
            return "{} hour(s), {} minute(s) left.".format(hours, minutes)
        else:
            return "{} day(s), {} hour(s), {} minute(s) left.".format(
                days, hours, minutes
            )
