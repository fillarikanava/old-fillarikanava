from django.template import Library
from django.utils.encoding import force_unicode

register = Library()

@register.filter
def in_group(user, groups):
    """Returns a boolean if the user is in the given group, or comma-separated
    list of groups.

    Usage::

        {% if user|in_group:"Friends" %}
        ...
        {% endif %}

    or::

        {% if user|in_group:"Friends,Enemies" %}
        ...
        {% endif %}

    """
    group_list = force_unicode(groups).split(',')
    return bool(user.groups.filter(name__in=group_list).values('name'))

@register.filter
def is_author(user, issue_author):
    try:
        profile = user.get_profile()
    except Exception:
        return False
    
    if profile.roundup_id == issue_author:
        return True
    else:
        return False