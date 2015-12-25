__author__ = 'ajay'

from datetime import datetime

MEMBER_TYPE = [
    ('temp', 'Temporary'),
    ('perm', 'Permanent')
]

YEAR_CHOICES = []
for r in range(1980, (datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

CITIES = (
    (None, '---Select Your Current City---'),
    ('Narela', 'Narela'),
    ('Gurgaon', 'Gurgaon'),
    ('Delhi', 'Delhi'),
    ('Noida', 'Noida'),
    ('Faridabad', 'Faridabad'),
)