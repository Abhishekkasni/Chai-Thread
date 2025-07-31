from django import template
from django.utils.timezone import now
# from datetime import timedelta

register = template.Library()

@register.filter
def twitter_time(value):
    """
    Formats a datetime like Twitter:
    - "just now" (under 1 min ago)
    - "Xm" (minutes, under 1 hour)
    - "Xh" (hours, under 1 day)
    - "Xd" (days, under 1 week)
    - "Jul 28" (over 7 days, same year)
    - "Jul 28, 2023" (older than a year)
    """

    if not value:
        return ""

    delta = now() - value

    # Under 1 minute ago
    if delta.total_seconds() < 60:
        return "just now"

    # Under 1 hour ago
    elif delta.total_seconds() < 3600:
        return f"{int(delta.total_seconds() // 60)}m"

    # Under 1 day ago
    elif delta.total_seconds() < 86400:
        return f"{int(delta.total_seconds() // 3600)}h"

    # Under 1 week ago
    elif delta.days < 7:
        return f"{delta.days}d"

    # Over a year ago — show full date with year
    elif value.year < now().year:
        return value.strftime("%b %d, %Y")  # e.g., "Jul 28, 2023"

    # Between 7 days and a year — show without year
    else:
        return value.strftime("%b %d")  # e.g., "Jul 28"

