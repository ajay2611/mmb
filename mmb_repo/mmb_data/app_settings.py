__author__ = 'naveen'

from datetime import datetime

SONG_TAGS = [
    ('love song', 'love song'),
]

CITIES = (
    (None, '---Select Your Current City---'),
    ('Narela', 'Narela'),
    ('Gurgaon', 'Gurgaon'),
    ('Delhi', 'Delhi'),
    ('Noida', 'Noida'),
    ('Faridabad', 'Faridabad'),
)

MEMBER_TYPE = [
    ('temp', 'Temporary'),
    ('perm', 'Permanent')
]
YEAR_CHOICES = []
for r in range(1980, (datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))
