from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.utils import timezone
from vanilla import CreateView, ListView, TemplateView
from functools import partial
from django.template import loader, Context
import plotlyChart as pc
import fitbitAPI as fb
import csv, os, json


# define decorators
from forms import ClinlibForm

from provider.models import *
from patient.views import SurveyView

def logged_in_and_in_group(user):
  r = False
  if user.is_authenticated():
    # group that user needs to be in
    if user.groups.filter(name='providerGroup').exists():
      r = True
  return r

class GroupRequiredMixin(object): 
  # path to be redirected when user is not logged in yet
  login_url = '/provider/'
  
  @method_decorator(user_passes_test(logged_in_and_in_group, login_url=login_url))
  # @method_decorator(user_passes_test(lambda u: u.is_superuser))
  def dispatch(self, *args, **kwargs):
    return super(GroupRequiredMixin, self).dispatch(*args, **kwargs)


class DashboardView(GroupRequiredMixin, generic.View):
  """DashboardView is the first view after login the provider sees"""
  # login_url = '/patient/'
  provider_list = [
    {'name': 'doctor sam', 'title': 'Othropedics','practice': 'Hospital for Special Surgery','has_warning': True},
    {'name': 'doctor pam', 'title': 'Geriatric','practice': 'Cornell Weill Hospital', 'has_warning': False}
  ]

  patient_list = [
     {'id':'123', 'name': 'John Doe', 'firstname': 'John', 'middlename': '','lastname':'Doe'},
     {'id':'4567', 'name': 'Jane Doe', 'firstname': 'Jane', 'middlename': '','lastname':'Doe'}

  ]






  def get(self, request):
    # return render_to_response('patient/dashboard.html', context_instance = RequestContext(request))
    user = request.user
    # user = ProviderProfile.get_provider_by_user(user)
    # user = ProviderProfile.objects.get(user = uid )

    pc.plotGraph()

    # if request.GET.__getitem__('exportcsv'):
    #   # render the file request
    #   self.exportfile(request)
    # genrate file
    

    return render(request,'provider/dashboard.html', 
      {"provider_list": self.provider_list,
        "patient_list": self.patient_list,
        "user": user
      } 
      )

def exportPSfile(request):
  # Create the HttpResponse object with the appropriate CSV header.

  # path_to_file = os.path.realpath("/Users/ahau/CarePigeon/provider/static/mHealth pilot data - 20150313.xlsx")
  path_to_file = os.path.realpath("/home/ubuntu/Care-pigeon.com/CarePigeon/provider/static/patient_mhealth.csv")
  f = open(path_to_file, 'r')
  

  # response = HttpResponse(f, content_type='application/vnd.ms-excel')
  # response['Content-Disposition'] = 'attachment; filename="HOOS_Steps.xlsx"'

  response = HttpResponse(f, content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="patient_mhealth.csv"'

  f.close()

  return response

def exportfitbitfile(request):
  # Create the HttpResponse object with the appropriate CSV header.
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="patient_steps.csv"'

  data = fb.getStepsTimeSeries('3m') 

  writer = csv.writer(response)
  for v in data:
    writer.writerow(v)

  return response

def exportSurveyResponseFile(request):
  # Create the HttpResponse object with the appropriate CSV header.
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="patient_survey_response.csv"'

  headers = [w['question_title'] for w in SurveyView.survey_structure['questions']]
  print headers

  data = PatientSurveyResponse.objects.all()
  for i in data:
    print type(i.response)
    print i.response
    # print i.response['Please indicate how often you performed running']



  writer = csv.writer(response)
  # write headers
  writer.writerow(['Response Date'] + headers)
  for v in data:
    row = []
    row.append(v.response_date)
    for j in headers:
      try:
        row.append(v.response[j])
      except:
        row.append('')
    writer.writerow(row)

  return response


class EducationView(GroupRequiredMixin, generic.View):
  """EducationView is where providers can customize eductaional content show their Clinical Library for patients"""
  # login_url = '/patient/'
  # select client lib * from client lib 


  education_list=[
    {'name': 'Frozen Shoulder', 'desc': 'General information on Frozen Shoulder', 'is_youtube': False, 'link':'http://someAMZNS3link'},
    {'name': 'Frozen Shoulder Video', 'desc': 'Video on Frozen Shoulder', 'is_youtube': True, 'link':'https://www.youtube.com/embed/q0S5EN7-RtI'}


  ]

  def get(self, request):
    # clinlib_form = ClinlibForm
    # return render_to_response('patient/dashboard.html', context_instance = RequestContext(request))
    return render(request,'provider/education.html', 
      {"education_list": self.education_list,
        "clinlib_form": ClinlibForm
      } 
      )

  def post(self, request):
    # parse request and save content to clinlib
    title = request.POST.get('title', False)
    desc = request.POST.get('desc', False)
    uri = request.POST.get('uri', False)
    # Clinlib.objects.create_content(title = title, desc = desc, uri = uri)


    return render(request,'provider/education.html', 
      {
        "education_list": self.education_list,
        "message" : 'Content: {} is added to your clinical library'.format(title)
        } 
      )

class ManageSurveyView(GroupRequiredMixin, generic.View):
  """EducationView is where providers can customize eductaional content for patients"""
  # login_url = '/patient/'
  survey_list=[
    {'name': 'Pedi-FABS', 'desc': 'Survey for pediatric sports activity and function', 'reminder_sent': 'weekly'},
    {'name': 'WOMAC', 'desc': 'Survey for hip and knee', 'reminder_sent': 'weekly' }

  ]

  def get(self, request):
    # return render_to_response('patient/dashboard.html', context_instance = RequestContext(request))
    return render(request,'provider/managesurvey.html', 
      {"survey_list": self.survey_list} 
      )

class ManagePatientView(GroupRequiredMixin, generic.View):
  """PatientView is where providers can manage their patients"""
  # login_url = '/patient/'
  patient_list=[
    {'id':'123','name': 'John Doe'},
    {'id':'456','name': 'Jane Doe'}

  ]

  def get(self, request):
    # return render_to_response('patient/dashboard.html', context_instance = RequestContext(request))
    return render(request,'provider/managepatient.html', 
      {"patient_list": self.patient_list} 
      )

class AddEditPatientView(GroupRequiredMixin, generic.View):
  """AddEditPatientView is where providers can add or edit the patient"""
  # login_url = '/patient/'
  patient ={'id':'123', 'name': 'John Doe', 'firstname': 'John', 'middlename': '','lastname':'Doe'}
  patient_assigned_surveys = [{'name':'Pedi-FABS' }]

  patient_assigned_content = [{'name':'Frozen Shoulder' }, {'name':'Frozen Shoulder Video'}]

  education_list=[
    {'name': 'Frozen Shoulder', 'desc': 'General information on Frozen Shoulder', 'is_youtube': False, 'link':'http://someAMZNS3link'},
    {'name': 'Frozen Shoulder Video', 'desc': 'Video on Frozen Shoulder', 'is_youtube': True, 'link':'https://www.youtube.com/embed/q0S5EN7-RtI'}
  ]

  survey_list=[
    {'name': 'Pedi-FABS', 'desc': 'Survey for pediatric sports activity and function', 'reminder_sent': 'weekly'},
    {'name': 'WOMAC', 'desc': 'Survey for hip and knee', 'reminder_sent': 'weekly' }

  ]
  

  def post(self, request, mode, pat_id):
    # return render_to_response('patient/dashboard.html', context_instance = RequestContext(request))
    return render(request,'provider/addeditpatient.html', 
      {
        "patient": self.patient,
        "patient_assigned_surveys": self.patient_assigned_surveys,
        "patient_assigned_content": self.patient_assigned_content,
        "education_list": self.education_list,
        "survey_list": self.survey_list
        }

      )











class ProviderDetailView(GroupRequiredMixin, generic.View):
  """PatientDetailView is the view after patient selects a specific provider"""
  # login_url = '/patient/'
  provider_detail_list ={
    'name': 'doctor sam', 
    'title': 'Othropedics',
    'practice': 'Hospital for Special Surgery',
    'has_warning': True
  }

  survey_token = '123'

  education_list=[
    {'name': 'Frozen Shoulder', 'desc': 'General information on Frozen Shoulder', 'is_youtube': False, 'link':'http://someAMZNS3link'},
    {'name': 'Frozen Shoulder Video', 'desc': 'Video on Frozen Shoulder', 'is_youtube': True, 'link':'https://www.youtube.com/embed/q0S5EN7-RtI'}


  ]

  def get(self, request):
    # return render_to_response('patient/dashboard.html', context_instance = RequestContext(request))
    return render(request,'provider/detail.html', 
      {"provider_list": self.provider_detail_list,
        "survey_token": self.survey_token,
        "education_list": self.education_list

        } 
      )

# class SurveyView(GroupRequiredMixin, generic.View):
#   """SurveyView handles loading the survey the patient needs to answer"""
#   survey_token = '123'
#   survey_structure = {
#     'name': 'Pedi-FABS',
#     'questions':[
#       {'question_title':'Please indicate how often you performed running', 
#         'question_id': '1',
#         'question_helper': '(running while playing a sport or jogging) in your healthiest and most active condition in the past month.',
#         'question_type': 'multiple-choice',
#         'question_choices': [{'choice': 'less than one time per month'},
#                               {'choice': 'one time per month'},
#                               {'choice': 'one time per week'},
#                               {'choice': '2-3 times per week'},
#                               {'choice': 'more than 4 times per week'}
#                             ]
#         },
#       {'question_title':'Please indicate how often you performed cutting', 
#         'question_id': '2',
#         'question_helper': '(quickly changing directions while running) in your healthiest and most active condition in the past month.',
#         'question_type': 'multiple-choice',
#         'question_choices': [{'choice': 'less than one time per month'},
#                               {'choice': 'one time per month'},
#                               {'choice': 'one time per week'},
#                               {'choice': '2-3 times per week'},
#                               {'choice': 'more than 4 times per week'}
#                             ]
#         },
#     ]

#   }
#   def get(self, request, survey_token):
#     # return render_to_response('patient/dashboard.html', context_instance = RequestContext(request))
#     return render(request,'provider/survey.html', 
#       {"survey_token": self.survey_token,
#         "survey_structure": self.survey_structure,
#         } 
#       )
    

