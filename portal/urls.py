from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from .views import *

urlpatterns = patterns('',
                       url(r'^$', ServiceListView.as_view(), name='service-list'),
                       url(r'^curso-de-xadrez/$', RedirectView.as_view(pattern_name='course:index'), name='course'),
                       url(r'^(?P<slug>[A-Za-z0-9_-]+)/$', ServiceDetailView.as_view(), name='service-detail'),
                       )
