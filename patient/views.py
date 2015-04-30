from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from vanilla import CreateView, ListView, TemplateView
from functools import partial
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# define decorators
from provider.models import *

def logged_in_and_in_group(user):
  r = False
  if user.is_authenticated():
    # group that user needs to be in
    if user.groups.filter(name='patientGroup').exists():
      r = True
  return r

class GroupRequiredMixin(object): 
  # path to be redirected when user is not logged in yet
  login_url = '/patient/'
  
  @method_decorator(user_passes_test(logged_in_and_in_group, login_url=login_url))
  # @method_decorator(user_passes_test(lambda u: u.is_superuser))
  def dispatch(self, *args, **kwargs):
    return super(GroupRequiredMixin, self).dispatch(*args, **kwargs)


class DashboardView(GroupRequiredMixin, generic.View):
  """DashboardView is the first view after login the patient sees"""
  # login_url = '/patient/'
  provider_list = [
    {'name': 'Dr. Taylor', 'imgsrc': '/static/patient/images/samtaylor.png', 'title': 'Orthopaedics, Sports Medicine & Shoulder','practice': 'Hospital for Special Surgery', 'is_flagged': True },
    {'name': 'Dr. O\'Brien', 'imgsrc': '/static/patient/images/stephenobrien.png', 'title': 'Orthopaedics, Sports Medicine & Shoulder','practice': 'Hospital for Special Surgery', 'is_flagged': False}
  ]

  def get(self, request):
    # return render_to_response('patient/dashboard.html', context_instance = RequestContext(request))
    return render(request,'patient/dashboard.html', 
      {"provider_list": self.provider_list} 
      )

class PatientDetailView(GroupRequiredMixin, generic.View):
  """PatientDetailView is the view after patient selects a specific provider"""
  # login_url = '/patient/'
  provider_detail_list ={
    'name': 'Dr. Taylor', 
    'title': 'Orthopaedics, Sports Medicine & Shoulder',
    'practice': 'Hospital for Special Surgery',
    # 'has_warning': True,
    'imgsrc': '/static/patient/images/samtaylor.png'
  }

  survey_token = '123'

  education_list=[
    {'name': 'Frozen Shoulder', 'desc': 'General information on Frozen Shoulder', 'is_read': False, 'is_youtube': False, 'link':'http://orthoinfo.aaos.org/PDFs/A00071.pdf'},
    {'name': 'Frozen Shoulder Video', 'desc': 'Video on Frozen Shoulder', 'is_read':True,'is_youtube': True, 'link':'https://www.youtube.com/embed/vJ-hm8bzOsk'}


  ]


  def get(self, request):
    # return render_to_response('patient/dashboard.html', context_instance = RequestContext(request))

    return render(request,'patient/detail.html', 
      {"provider_list": self.provider_detail_list,
        "survey_token": self.survey_token,
        "education_list": self.education_list

        } 
      )

class SurveyView(GroupRequiredMixin, generic.View):
  """SurveyView handles loading the survey the patient needs to answer"""
  survey_token = '123'
  # survey_structure = {
  #   'name': 'Pedi-FABS',
  #   'questions':[
  #     {'question_title':'Please indicate how often you performed running', 
  #       'question_id': '1',
  #       'question_helper': '(running while playing a sport or jogging) in your healthiest and most active condition in the past month.',
  #       'question_type': 'multiple-choice',
  #       'question_choices': [{'choice': 'less than one time per month'},
  #                             {'choice': 'one time per month'},
  #                             {'choice': 'one time per week'},
  #                             {'choice': '2-3 times per week'},
  #                             {'choice': 'more than 4 times per week'}
  #                           ]
  #       },
  #     {'question_title':'Please indicate how often you performed cutting', 
  #       'question_id': '2',
  #       'question_helper': '(quickly changing directions while running) in your healthiest and most active condition in the past month.',
  #       'question_type': 'multiple-choice',
  #       'question_choices': [{'choice': 'less than one time per month'},
  #                             {'choice': 'one time per month'},
  #                             {'choice': 'one time per week'},
  #                             {'choice': '2-3 times per week'},
  #                             {'choice': 'more than 4 times per week'}
  #                           ]
  #       },
  #   ]
  # }

  survey_structure = {
    'name': 'KOOS Jr',
    'questions':[
      {'question_title':'In the last week, how severe is your knee stiffness after first wakening in the morning?', 
        'question_id': '1',
        'question_helper': '',
        'question_type': 'multiple-choice',
        'question_choices': [{'choice': 'none'},
                              {'choice': 'mild'},
                              {'choice': 'moderate'},
                              {'choice': 'severe'},
                              {'choice': 'extreme'}
                            ]
        },
      {'question_title':'What amount of knee pain have you experienced the last week twisting/pivoting on your knee?', 
        'question_id': '2',
        'question_helper': '',
        'question_type': 'multiple-choice',
        'question_choices': [{'choice': 'none'},
                              {'choice': 'mild'},
                              {'choice': 'moderate'},
                              {'choice': 'severe'},
                              {'choice': 'extreme'}
                            ]
        },
      {'question_title':'What amount of knee pain have you experienced the last week straightening your knee fully?', 
        'question_id': '3',
        'question_helper': '',
        'question_type': 'multiple-choice',
        'question_choices': [{'choice': 'none'},
                              {'choice': 'mild'},
                              {'choice': 'moderate'},
                              {'choice': 'severe'},
                              {'choice': 'extreme'}
                            ]
        },
      {'question_title':'What amount of knee pain have you experienced the last week going up or down stairs?', 
        'question_id': '4',
        'question_helper': '',
        'question_type': 'multiple-choice',
        'question_choices': [{'choice': 'none'},
                              {'choice': 'mild'},
                              {'choice': 'moderate'},
                              {'choice': 'severe'},
                              {'choice': 'extreme'}
                            ]
        },
      {'question_title':'What amount of knee pain have you experienced the last week standing upright?', 
        'question_id': '5',
        'question_helper': '',
        'question_type': 'multiple-choice',
        'question_choices': [{'choice': 'none'},
                              {'choice': 'mild'},
                              {'choice': 'moderate'},
                              {'choice': 'severe'},
                              {'choice': 'extreme'}
                            ]
        },
      {'question_title':'Please indicate the degree of difficulty you have experienced in the last week due to your knee in rising from sitting:', 
        'question_id': '6',
        'question_helper': '',
        'question_type': 'multiple-choice',
        'question_choices': [{'choice': 'none'},
                              {'choice': 'mild'},
                              {'choice': 'moderate'},
                              {'choice': 'severe'},
                              {'choice': 'extreme'}
                            ]
        },
      {'question_title':'Please indicate the degree of difficulty you have experienced in the last week due to your knee in bending to floor/picking up an object:', 
        'question_id': '7',
        'question_helper': '',
        'question_type': 'multiple-choice',
        'question_choices': [{'choice': 'none'},
                              {'choice': 'mild'},
                              {'choice': 'moderate'},
                              {'choice': 'severe'},
                              {'choice': 'extreme'}
                            ]
        },
      {'question_title':'Please indicate the degree of difficulty you have experienced in the last week due to your knee going shopping:', 
        'question_id': '8',
        'question_helper': '',
        'question_type': 'multiple-choice',
        'question_choices': [{'choice': 'none'},
                              {'choice': 'mild'},
                              {'choice': 'moderate'},
                              {'choice': 'severe'},
                              {'choice': 'extreme'}
                            ]
        }
    ]
  }

  def get(self, request, survey_token):
    # return render_to_response('patient/dashboard.html', context_instance = RequestContext(request))
    return render(request,'patient/survey.html', 
      {"survey_token": self.survey_token,
        "survey_structure": self.survey_structure,
        } 
      )

  def post(self, request, survey_token):
    # print request.POST['Please indicate how often you performed running']
    # print request
    # save results back to DB

    patient_id = PatientProfile.objects.get(user = request.user)
    survey_id = SurveyLib.objects.get(title = 'KoosJr')


    p = PatientSurveyResponse.objects.create(patient_id = patient_id, survey_id = survey_id, response = request.POST)


    return redirect('/patient/detail?s=1' 
      )



def get_pagination_page(page=1):
    items = range(0, 100)
    paginator = Paginator(items, 10)
    try:
        page = int(1)
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)

    return items
    

