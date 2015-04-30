# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinlib',
            fields=[
                ('clinlib_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('desc', models.CharField(max_length=8000)),
                ('is_youtube', models.BooleanField(default=False)),
                ('uri', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClinLibPatientLookup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clinlib_id', models.ForeignKey(to='provider.Clinlib')),
                ('patient_id', models.ForeignKey(to='patient.PatientProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientSurveyLookup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_id', models.ForeignKey(to='patient.PatientProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientSurveyResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('response_date', models.DateTimeField(verbose_name=b'Response Date')),
                ('response', jsonfield.fields.JSONField(verbose_name=b'Survey Response JSON')),
                ('patient_id', models.ForeignKey(to='patient.PatientProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProviderPatientLookup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_id', models.ForeignKey(to='patient.PatientProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProviderProfile',
            fields=[
                ('provider_id', models.AutoField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('practice', models.CharField(max_length=200)),
                ('imgsrc', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProviderSurveyLookup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reminder_frequency', models.CharField(default=b'M', max_length=2, choices=[(b'D', b'Daily'), (b'W', b'Weekly'), (b'M', b'Monthly')])),
                ('provider_id', models.ForeignKey(to='provider.ProviderProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SurveyLib',
            fields=[
                ('survey_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('surevy_structure', jsonfield.fields.JSONField(verbose_name=b'Survey Structure JSON')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='providersurveylookup',
            name='survey_id',
            field=models.ForeignKey(to='provider.SurveyLib'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='providerpatientlookup',
            name='provider_id',
            field=models.ForeignKey(to='provider.ProviderProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patientsurveyresponse',
            name='survey_id',
            field=models.ForeignKey(to='provider.SurveyLib'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patientsurveylookup',
            name='survey_id',
            field=models.ForeignKey(to='provider.SurveyLib'),
            preserve_default=True,
        ),
    ]
