# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, UpdateView, DetailView, RedirectView, FormView, ListView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from datetime import date
from utils.permissions import LoginRequiredMixin
from extra_views import CreateWithInlinesView, InlineFormSet
from pagseguro.api import PagSeguroItem, PagSeguroApi
from .models import Competitor, CompetitorsResponsible
from .forms import CompetitorsResponsibleForm, CompetitorForm, DepositPaymentForm, CheckInscriptionForm


class ChessFestivalTournament(TemplateView):

    template_name = "tournament/chessfestivaltournament.html"

    def get_context_data(self, **kwargs):
        kwargs = super(ChessFestivalTournament, self).get_context_data(**kwargs)
        today = date.today()
        tournament_date = date(2015, 12, 06)
        left_days = tournament_date - today
        kwargs['inscription_today'] = None
        if left_days.days > 0:
            kwargs['left_days'] = left_days.days
        else:
            kwargs['left_days'] = u'É hoje!'
            kwargs['inscription_today'] = u'Inscrições para o Absoluto até as 13h30 de %s no local' % today.strftime('%d/%m/%Y')
        kwargs['competitors_number'] = Competitor.objects.count()

        return kwargs


class CompetitorInlineFormset(InlineFormSet):
    model = Competitor
    form_class = CompetitorForm
    extra = 1

    def get_factory_kwargs(self):
        kwargs = super(CompetitorInlineFormset, self).get_factory_kwargs()
        kwargs.update({
            "min_num": 1,
            "validate_min": True
        })
        return kwargs


class TournamentInscription(CreateWithInlinesView):
    """ """
    model = CompetitorsResponsible
    form_class = CompetitorsResponsibleForm
    inlines = [CompetitorInlineFormset, ]
    template_name = 'tournament/tournamentinscription_form.html'

    def get_success_url(self):
        self.request.session['t_inscription'] = self.object.pk
        self.request.session.set_expiry(0)
        return reverse('tournament:checkout', kwargs={'pk': self.object.pk})

    def forms_valid(self, form, inlines):
        form.inscription_mail()
        return super(TournamentInscription, self).forms_valid(form, inlines)


class TournamentCheckoutView(UpdateView):
    """
    """
    model = CompetitorsResponsible
    form_class = DepositPaymentForm
    template_name = "tournament/tournament_checkout.html"
    initial = {'payment_type': '2'}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if self.object.paid:
            messages.info(self.request, 'Sua inscrição já está confirmada. Não precisa pagar de novo ;)')
            messages.info(self.request, 'Por que não aproveita e convida um amigo para jogar também?! :D')
            redirect('tournament:chessfestival')

        inscription_id = self.request.session.get("t_inscription", "")
        if (not inscription_id) or (inscription_id != self.object.pk):
            raise Http404

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        kwargs = super(TournamentCheckoutView, self).get_context_data(**kwargs)

        if self.object.competitors.count() == 0:
            messages.error(self.request, 'Você precisa cadastrar pelo menos um competidor')
            return redirect('tournament:inscription')

        tournament_price = self.object.competition.price
        qtd = self.object.competitors.count()
        total = qtd * tournament_price
        kwargs.update(inscription=self.object, total=total)

        return kwargs

    def get_success_url(self):
        return reverse('tournament:pre-inscription', kwargs={'pk': self.object.pk})


class PreInscription(DetailView):

    model = CompetitorsResponsible
    template_name = 'tournament/preinscription.html'

    def get_context_data(self, **kwargs):
        kwargs = super(PreInscription, self).get_context_data(**kwargs)
        total = self.object.competitors.count() * self.object.competition.price
        kwargs['total'] = total
        kwargs['inscription_number'] = '{0:03d}'.format(self.object.pk)
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        obj = context['object']

        if obj.paid:
            raise Http404
        if obj.pk != self.request.session.get('t_inscription'):
            raise Http404
        else:
            del self.request.session['t_inscription']
            return super(PreInscription, self).render_to_response(context, **response_kwargs)


class TournamentPagseguroReturn(TemplateView):

    template_name = "tournament/pagseguro_return.html"

    def get_data(self, pid):
        if not pid:
            return
        pg = PagSeguroApi()
        data = pg.get_transaction(pid)
        if data['success']:
            self.reference = int(data['transaction']['reference'])
            payment_status = str(data['transaction']['status'])
            self.update_transaction_status('status', payment_status)

            if payment_status == "3":
                self.update_transaction_status('paid', True)

            return data
        return {}

    def get_inscription(self):
        if not self.reference:
            raise Http404

        if hasattr(self, 'obj'):
            return self.obj

        self.obj = get_object_or_404(CompetitorsResponsible, pk=self.reference)
        return self.obj

    def update_transaction_status(self, param, value):
        obj = self.get_inscription()
        setattr(obj, param, value)
        obj.save()
        return

    def get_context_data(self, **kwargs):
        kwargs = super(TournamentPagseguroReturn, self).get_context_data(**kwargs)

        pid = self.request.GET.get("pid", "")
        if not pid:
            raise Http404

        data = self.get_data(pid)
        if data:
            kwargs.update(data)

        obj = self.get_inscription()
        kwargs.update({'inscription': obj})
        if not obj.transaction:
            self.update_transaction_status('transaction', pid)

        return kwargs


class PagseguroPayment(RedirectView):

    def pagseguro(self, inscription):
        obj = get_object_or_404(CompetitorsResponsible, pk=inscription)
        item = PagSeguroItem(
            id=obj.competition.pk,
            description=obj.competition.name,
            amount=obj.competition.price,
            quantity=obj.competitors.count()
        )
        pg = PagSeguroApi(
            reference=obj.pk,
            senderEmail=obj.email
        )
        pg.add_item(item)
        data = pg.checkout()
        if data.get('success'):
            return data['redirect_url']
        else:
            messages.error(self.request, "Houve um erro ao processar seus dados. Se o problema persistir entre em contato: (61) 8121-7870 ou (61) 9193-0933")
            return reverse("tournament:checkout")

    def get_redirect_url(self, *args, **kwargs):
        obj = int(kwargs['pk'])
        if obj != self.request.session.get('t_inscription'):
            raise Http404
        else:
            url = self.pagseguro(obj)
        return url


class UpdatePaymentView(TemplateView):

    template_name = 'tournament/update_payment.html'
    http_method_names = ['post', ]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdatePaymentView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        notification = self.request.POST.get('notificationCode')
        pg = PagSeguroApi()
        pg.get_notification(notification)
        return HttpResponse('Dados atualizados')


class RegulamentoView(TemplateView):

    template_name = 'tournament/regulamento.html'


class CheckInscription(FormView):
    """
    """
    form_class = CheckInscriptionForm
    template_name = 'tournament/check_inscription.html'

    def get_context_data(self, **kwargs):
        kwargs = super(CheckInscription, self).get_context_data(**kwargs)
        email = self.request.session.get('inscription_email')
        if email:
            kwargs['inscription_email'] = email
            kwargs['competitors'] = CompetitorsResponsible.objects.prefetch_related('competitors').filter(email=email)
            # del self.request.session['inscription_email']
        return kwargs

    def form_valid(self, form):
        self.request.session['inscription_email'] = form.cleaned_data['email']
        messages.info(self.request, u'Informações obtidas. Confira o resultado abaixo.')
        return super(CheckInscription, self).form_valid(form)

    def get_success_url(self):
        return reverse('tournament:check_inscription')


class RelacaoInscritos(TemplateView):

    template_name = 'tournament/inscritos.html'


class InscritosCategoria(TemplateView):

    template_name = 'tournament/inscritos_categoria.html'

    def get_context_data(self, **kwargs):
        kwargs = super(InscritosCategoria, self).get_context_data(**kwargs)
        kwargs['count'] = len(Competitor.modality.categoria())
        kwargs['sub_7'] = Competitor.modality.sub_7()
        kwargs['sub_9'] = Competitor.modality.sub_9()
        kwargs['sub_12'] = Competitor.modality.sub_12()
        kwargs['sub_15'] = Competitor.modality.sub_15()
        kwargs['sub_18'] = Competitor.modality.sub_18()
        return kwargs


class InscritosAbsoluto(TemplateView):

    template_name = 'tournament/inscritos_absoluto.html'

    def get_context_data(self, **kwargs):
        kwargs = super(InscritosAbsoluto, self).get_context_data(**kwargs)
        competitors = Competitor.modality.absoluto()
        kwargs['competitors'] = competitors
        return kwargs


class RegulamentoCategoria(TemplateView):

    template_name = 'tournament/regulamento_categoria.html'


class RegulamentoAbsoluto(TemplateView):

    template_name = 'tournament/regulamento_absoluto.html'


class DashboardListInscriptions(LoginRequiredMixin, ListView):

    model = Competitor
    template_name = 'tournament/dash_list_inscription.html'
