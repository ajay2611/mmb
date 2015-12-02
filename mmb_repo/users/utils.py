__author__ = 'naveen'
import os
from django.core.exceptions import ValidationError
import re

from config.settings.common import MEDIA_ROOT



def handle_uploaded_file(f, pk):
    """
    uploading file to a specific folder based on user
    :param f: mp3 file
    :param pk: user primary key
    :return:
    """
    pk = unicode(pk)
    folder = pk
    audio = "audio"
    try:
        os.mkdir(os.path.join(MEDIA_ROOT, audio))
        os.mkdir(os.path.join(MEDIA_ROOT, audio, folder))
    except:
        pass

    name_list = os.path.splitext(f.name)
    ext = name_list[-1]
    name = name_list[0]
    full_path = os.path.join(MEDIA_ROOT, audio, folder)

    destination = open('{0}/{1}{2}'.format(full_path, name, ext), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


# def comma_pin_validator(value):
#     value = value.replace(" ", ",")
#     all_values = value.split(',')
#     error = False
#     for each in all_values:
#         if not len(each) == 6:
#             error = True
#             break
#         try:
#             pin_int = int(each)
#             type(pin_int) == int
#         except ValueError:
#             error = True
#             break
#     if error:
#         raise ValidationError(u'%s is not a valid Pin-Code' % value)

#
# website_regex = re.compile(
#         r'^(?:http|ftp)s?://' # http:// or https://
#         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
#         # r'localhost|' #localhost...
#         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
#         r'(?::\d+)?' # optional port
#         r'(?:/?|[/?]\S+)$', re.IGNORECASE)
