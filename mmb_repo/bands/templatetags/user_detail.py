__author__ = 'naveen'
from django import template
register = template.Library()
from mmb_repo.users.models import Profile

@register.simple_tag
def user_detail(user_id, type=None):
    list = []
    try:
        obj = Profile.objects.get(user__id=user_id)

        if type == 'Instrument':
            list = obj.instrument.values_list('instrument', flat=True)

        if type == 'Genre':
            list = obj.genre.values_list('genre', flat=True)

    except:
        return []

    if not type:
        return obj
    else:
        return list

register.filter('user_detail', user_detail)
