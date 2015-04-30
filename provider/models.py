from django.db import models
from jsonfield import JSONField
from patient.models import PatientProfile
from django.contrib.auth.models import User
from datetime import datetime  

# Create your models here.


class ProviderProfile(models.Model):
  def __unicode__(self):
    return u'%s %s %s' % (self.first_name, self.middle_name, self.last_name)

  provider_id = models.AutoField(primary_key=True)
  first_name = models.CharField(max_length=200)
  middle_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  title = models.CharField(max_length=200)
  practice = models.CharField(max_length=200)
  imgsrc = models.CharField(max_length=500)
  user = models.ForeignKey(User, unique=True)

class ProviderProfileManager(models.Manager):
  def create_provider(self, first_name, middle_name, last_name, title, practice, imgsrc):
      provider = self.create(first_name = first_name, middle_name = middle_name, last_name = last_name, title = title, practice = practice, imgsrc = imgsrc)
      # do something with the patient
      return provider
  def get_provider_by_user(self, user):
      return self.objects.get(user = user)
      # objects.get(pk=1)



class ProviderPatientLookup(models.Model):
  def __unicode__(self):
    return u'%s %s' % (self.patient_id, self.provider_id)
  patient_id = models.ForeignKey(PatientProfile)
  provider_id = models.ForeignKey(ProviderProfile)
  # provider_id = models.CharField(max_length=200)

class Clinlib(models.Model):
  def __unicode__(self):
    return u'%s %s %s' % (self.first_name, self.middle_name, self.last_name)

  clinlib_id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=500)
  desc = models.CharField(max_length=8000)
  is_youtube = models.BooleanField(default = False)
  uri = models.CharField(max_length=1000)

class ClinlibManager(models.Manager):
  def create_content(self, title, desc, uri):
    is_youtube = False
    if 'youtube.com' in uri:
      is_youtube = True
    content = self.create(title = title, desc = desc , is_youtube = is_youtube, uri = uri )
    return content


class ClinLibPatientLookup(models.Model):
  def __unicode__(self):
    return u'%s %s' % (self.patient_id, self.clinlib_id)
  patient_id = models.ForeignKey(PatientProfile)
  clinlib_id = models.ForeignKey(Clinlib)

class SurveyLib(models.Model):
  def __unicode__(self):
    return u'%s' % (self.title)

  survey_id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=200)
  surevy_structure = JSONField('Survey Structure JSON')

class PatientSurveyLookup(models.Model):
  def __unicode__(self):
    return u'%s %s' % (self.patient_id, self.survey_id)


  patient_id = models.ForeignKey(PatientProfile)
  survey_id = models.ForeignKey(SurveyLib)


class ProviderSurveyLookup(models.Model):
  def __unicode__(self):
    return u'%s %s' % (self.patient_id, self.survey_id)


  daily = 'D'
  weekly = 'W'
  monthly = 'M'

  reminder_frequency_choices = (
    (daily, 'Daily'),
    (weekly, 'Weekly'),
    (monthly, 'Monthly')
    )

  provider_id = models.ForeignKey(ProviderProfile)
  survey_id = models.ForeignKey(SurveyLib)
  reminder_frequency = models.CharField(max_length=2, choices = reminder_frequency_choices, default = monthly)


class PatientSurveyResponse(models.Model):
  def __unicode__(self):
    return u'%s %s' % (self.patient_id, self.response_date)

  patient_id = models.ForeignKey(PatientProfile)
  survey_id = models.ForeignKey(SurveyLib)
  response_date = models.DateTimeField('Response Date', default=datetime.now)
  response = JSONField('Survey Response JSON')

# class PatientSurveyResponseManager(models.Manager):
#   def answer_survey(self, patient_id, survey_id, response):
#     answer = self.create(patient_id, survey_id, response)
#     return answer

