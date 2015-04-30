from django.forms import ModelForm
from django import forms
from provider.models import *

class ClinlibForm(ModelForm):
  title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter a title...'}))


  class Meta:
    model = Clinlib
    fields = ['title', 'desc', 'uri']