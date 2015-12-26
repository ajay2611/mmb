__author__ = 'naveen'
from django import template
register = template.Library()
from mmb_repo.mmb_data.models import UserFollowers

@register.simple_tag
def check_follow(active_user, user):
    success = False
    try:
        obj = UserFollowers.objects.get(follower=active_user, following=user)
        if obj:
            success = True
    except:
        success = False

    return success

register.filter('check_follow', check_follow)
