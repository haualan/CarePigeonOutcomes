# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('patient_id', models.AutoField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('date_of_birth', models.DateTimeField(verbose_name=b'Date of Birth')),
                ('date_of_surgery', models.DateTimeField(verbose_name=b'Date of Surgery')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
