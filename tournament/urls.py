from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
                       # url(r'^festival-de-xadrez/inscricao/$', TournamentInscription.as_view(), name='inscription'),
                       url(r'^festival-de-xadrez/pre-inscricao/(?P<pk>\d+)/$', PreInscription.as_view(), name='pre-inscription'),
                       url(r'^festival-de-xadrez/checkout/(?P<pk>\d+)/$', TournamentCheckoutView.as_view(), name='checkout'),
                       url(r'^festival-de-xadrez/pagamento/(?P<pk>\d+)/$', PagseguroPayment.as_view(), name='payment'),
                       url(r'^festival-de-xadrez/pagamento/concluido/$', TournamentPagseguroReturn.as_view(), name='payment_finished'),
                       url(r'^festival-de-xadrez/pagamento/atualizacao/$', UpdatePaymentView.as_view(), name='payment_updated'),
                       url(r'^festival-de-xadrez/regulamento/$', RegulamentoView.as_view(), name='regulamento'),
                       url(r'^festival-de-xadrez/checar-inscricao/$', CheckInscription.as_view(), name='check_inscription'),
                       url(r'^festival-de-xadrez/gerenciar/list$', DashboardListInscriptions.as_view(), name='dash_list_inscription'),
                       url(r'^festival-de-xadrez/inscritos/$', RelacaoInscritos.as_view(), name='inscritos'),
                       url(r'^festival-de-xadrez/inscritos/categoria/$', InscritosCategoria.as_view(), name='inscritos_cat'),
                       url(r'^festival-de-xadrez/inscritos/absoluto/$', InscritosAbsoluto.as_view(), name='inscritos_abs'),
                       url(r'^festival-de-xadrez/$', ChessFestivalTournament.as_view(), name='chessfestival'),
                       )
