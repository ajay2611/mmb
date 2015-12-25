# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mmb_data', '0003_auto_20151225_1030'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('location', models.CharField(blank=True, max_length=50, null=True, choices=[(None, b'---Select Your Current City---'), (b'Narela', b'Narela'), (b'Gurgaon', b'Gurgaon'), (b'Delhi', b'Delhi'), (b'Noida', b'Noida'), (b'Faridabad', b'Faridabad')])),
                ('label', models.CharField(max_length=50, null=True, blank=True)),
                ('year', models.IntegerField(default=2015, verbose_name=b'year', choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)])),
                ('about_me', models.CharField(max_length=255, null=True, blank=True)),
                ('genre', models.ManyToManyField(to='mmb_data.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='BandMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'temp', max_length=4, choices=[(b'temp', b'Temporary'), (b'perm', b'Permanent')])),
                ('band', models.ForeignKey(to='bands.Band')),
                ('instrument', models.ForeignKey(to='mmb_data.Instrument')),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='band',
            name='member',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='bands.BandMember'),
        ),
    ]
