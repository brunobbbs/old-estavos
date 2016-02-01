# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.utils.translation import ugettext as _

from portal.views import (AboutUsView, ContactView, HomePageView,
                          WorkWithUsCreateView)


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^retorno/pagseguro/', include('pagseguro.urls')),
                       url(r'^tinymce/', include('tinymce.urls')),  # TinyMCE URLs
                       url(r'^summernote/', include('django_summernote.urls')),
                       url(r'^accounts/', include('account.urls', namespace='accounts')),
                       url(r'^servicos/', include('portal.urls', namespace='services')),
                       url(r'^quem-somos/$', AboutUsView.as_view(), name='about-us'),
                       url(r'^contato/$', ContactView.as_view(), name='contato'),
                       url(r'^trabalhe-conosco/$', WorkWithUsCreateView.as_view(), name='workwithus'),
                       url(r'^painel/', include('esap.urls', namespace='dashboard')),
                       url(r'^curso-de-xadrez/', include('course.urls', namespace='course')),
                       # url(r'^torneios/', include('tournament.urls', namespace='tournament')),
                       url(r'^$', HomePageView.as_view(), name='home'),
                       )

admin.site.site_title = _(u"Academia ESTAVOS")
admin.site.site_header = _(u"Administração do site - Academia ESTAVOS")

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT, }),
                            )
