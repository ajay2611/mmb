__author__ = 'ajay'

from datetime import datetime

MEMBER_TYPE = [
    ('perm', 'Permanent'),
    ('temp', 'Temporary')
]

YEAR_CHOICES = [(r,r) for r in range(1980, (datetime.now().year+1))]

CITIES = (
    (None, '---Select Your Current City---'),
    ('Narela', 'Narela'),
    ('Gurgaon', 'Gurgaon'),
    ('Delhi', 'Delhi'),
    ('Noida', 'Noida'),
    ('Faridabad', 'Faridabad'),
)