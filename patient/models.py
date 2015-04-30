from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
# from provider.models import ProviderProfile, ClinLib

class PatientProfile(models.Model):
  def __unicode__(self):
    return u'%s %s %s' % (self.first_name, self.middle_name, self.last_name)

  patient_id = models.AutoField(primary_key=True)
  first_name = models.CharField(max_length=200)
  middle_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  date_of_birth = models.DateTimeField('Date of Birth')
  date_of_surgery = models.DateTimeField('Date of Surgery')
  user = models.ForeignKey(User, unique=True)
  # settings.AUTH_USER_MODEL
  email = models.EmailField(max_length=254, default= 'patient@noemail.com')

class PatientProfileManager(models.Manager):
    def create_patient(self, first_name, middle_name, last_name, date_of_birth, date_of_surgery):
        patient = self.create(first_name = first_name, middle_name = middle_name, last_name = last_name, date_of_birth = date_of_birth, date_of_surgery = date_of_surgery)
        # do something with the patient
        return patient

# class BookManager(models.Manager):
#     def create_book(self, title):
#         book = self.create(title=title)
#         # do something with the book
#         return book

# class Book(models.Model):
#     title = models.CharField(max_length=100)

#     objects = BookManager()

# book = Book.objects.create_book("Pride and Prejudice")