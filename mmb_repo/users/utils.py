__author__ = 'naveen'
from django.core.exceptions import ValidationError
import re

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
