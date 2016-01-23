__author__ = 'naveen'
from django import template
register = template.Library()
from mmb_repo.bands.models import BandFollowers

@register.simple_tag
def check_band_follow(user, band):
    success = False
    try:
        obj = BandFollowers.objects.get(follower=user, following_band=band)
        if obj:
            success = True
    except:
        success = False

    return success

register.filter('check_band_follow', check_band_follow)
