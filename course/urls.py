from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
                       url(r'^$', CourseView.as_view(), name='index'),
                       url(r'^inscricao/$', CourseSubscriptionView.as_view(), name='subscription'),
                       url(r'^pagamento/checkout/$', CourseCheckoutView.as_view(), name='checkout'),
                       url(r'^pagamento/conclusao/$', CoursePagseguroReturn.as_view(), name='pagseguro_done'),
                       url(r'^pagamento/$', PagseguroPayment.as_view(), name='pagseguro_payment'),
                       )
