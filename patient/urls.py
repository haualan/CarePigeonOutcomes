from django.conf.urls import patterns, url, include
from patient import views
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


dajaxice_autodiscover()

urlpatterns = patterns('',
  # url(r'^$', views.IndexView.as_view(), name='index'),
  url(r'^$', 'django.contrib.auth.views.login',{'template_name': 'patient/index.html'}, name='index'),
  url(r'^dashboard$', views.DashboardView.as_view(), name='dashboard'),
  url(r'^detail$', views.PatientDetailView.as_view(), name='detail'),
  url(r'^survey/(?P<survey_token>\d+)$', views.SurveyView.as_view(), name='survey'),
  url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
  # url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
  # url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
  # url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
  # url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'patient/dashboard.html'}, name = 'login'),
  url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/patient/'}, name = 'logout'),
  url(r'^ajax$', views.get_pagination_page, name = 'ajax'),
)

urlpatterns += staticfiles_urlpatterns()