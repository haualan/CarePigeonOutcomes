# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_patientprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientprofile',
            name='email',
            field=models.EmailField(default=b'patient@noemail.com', max_length=254),
            preserve_default=True,
        ),
    ]
