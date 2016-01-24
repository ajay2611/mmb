from django import template
register = template.Library()
from mmb_repo.bands.models import BandMember


@register.assignment_tag
def change_profile(user):
    data = {}
    bandmembers = BandMember.objects.filter(member=user)
    for bandmember in bandmembers:
        id = bandmember.band.id
        name = bandmember.band.name
        data.update({id: name})
    return data

register.filter('change_profile', change_profile)
