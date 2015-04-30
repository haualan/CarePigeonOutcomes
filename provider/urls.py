from django.conf.urls import patterns, url

from provider import views

urlpatterns = patterns('',
  # url(r'^$', views.IndexView.as_view(), name='index'),
  url(r'^$', 'django.contrib.auth.views.login',{'template_name': 'provider/index.html'}, name='index'),
  url(r'^dashboard$', views.DashboardView.as_view(), name='dashboard'),
  url(r'^exportfitbitfile$', views.exportfitbitfile, name='exportfitbitfile'),
  url(r'^exportPSfile$', views.exportPSfile, name='exportPSfile'),
  url(r'^exportSurveyResponseFile$', views.exportSurveyResponseFile, name='exportSurveyResponseFile'),
  url(r'^education$', views.EducationView.as_view(), name='education'),
  url(r'^managesurvey$', views.ManageSurveyView.as_view(), name='manageSurvey'),
  url(r'^managepatient$', views.ManagePatientView.as_view(), name='managePatient'),
  url(r'^addeditpatient/(?P<mode>\w+)/(?P<pat_id>\d+)$', views.AddEditPatientView.as_view(), name='addEditPatient'),


  # url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
  # url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
  # url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
  # url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'patient/dashboard.html'}, name = 'login'),
  url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/provider/'}, name = 'logout'),
)