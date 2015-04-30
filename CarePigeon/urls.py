from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^patient/', include('patient.urls', namespace="patient")),
    url(r'^provider/', include('provider.urls', namespace="provider")),
)
