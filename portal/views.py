# -*- coding: utf-8 -*-

from django.contrib import messages
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views import generic

from portal.forms import ContactForm, TalentForm
from portal.models import AboutUs, Service, Talent, Testimonial


class HomePageView(generic.TemplateView):
    """ """
    template_name = 'portal/index.html'

    def __split_list(self, lst):
        half = len(lst) / 2
        return lst[:half], lst[half:]

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        services = Service.objects.all()
        context['services_1'], context['services_2'] = self.__split_list(services)
        context['testimonials'] = Testimonial.objects.all()
        return context


class ServiceDetailView(generic.DetailView):
    """ """
    model = Service
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)
        obj = context['object']
        context['gallery'] = obj.gallery.images.all()
        return context


class ServiceListView(generic.ListView):
    """ """
    model = Service


class AboutUsView(generic.TemplateView):
    """ """
    template_name = 'portal/about-us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)

        try:
            qs = AboutUs.objects.all()[0]
        except IndexError:
            raise Http404

        context['object'] = qs
        context['gallery'] = qs.gallery.images.all()
        return context


class ContactView(generic.edit.FormView):
    """ """
    # https://docs.djangoproject.com/en/1.7/ref/class-based-views/generic-editing/
    template_name = 'portal/contact_view.html'
    form_class = ContactForm
    success_url = '/contato/'

    def form_valid(self, form):
        form.send_mail()
        messages.success(
            self.request,
            _(u"Obrigado! Sua mensagem foi enviada com sucesso!")
        )
        messages.success(
            self.request,
            _(u"Aguarde que em breve um de nossos consultores entrará em contato com você!")
        )
        return super(ContactView, self).form_valid(form)


class WorkWithUsCreateView(generic.edit.CreateView):
    """ """
    model = Talent
    template_name = 'portal/workwithus_view.html'
    form_class = TalentForm
    success_url = '/trabalhe-conosco/'

    def form_valid(self, form):
        messages.success(
            self.request,
            _(u"Seus dados foram enviados com sucesso!")
        )
        return super(WorkWithUsCreateView, self).form_valid(form)
