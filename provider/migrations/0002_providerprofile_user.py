# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='providerprofile',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=False,
        ),
    ]
