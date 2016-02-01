# -*- coding: utf-8 -*-

from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from utils.ajax import AjaxableResponseMixin
from utils.permissions import LoginRequiredMixin, PermissionsRequiredMixin
from utils.mixin import JSONResponseMixin

from .forms import *
from .models import *

from tournament.models import Competitor

from extra_views import InlineFormSet, UpdateWithInlinesView


# Dashboard

class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "esap/index.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['classes_count'] = Classes.objects.all().count()
        context['modules_count'] = Module.objects.all().count()
        context['festival_inscriptions'] = Competitor.objects.all().count()
        return context


# SupportMaterial

class SupportMaterialFormSet(InlineFormSet):
    model = SupportMaterial
    form_class = SupportMaterialForm
    extra = 1


# Classes

class ClassesListView(PermissionsRequiredMixin, generic.ListView):
    required_permissions = (
        'esap.view_classes',
    )
    model = Classes
    paginate_by = 10


class ClassesCreateAjaxFormView(PermissionsRequiredMixin, generic.FormView):
    required_permissions = (
        'esap.add_classes',
    )
    form_class = ClassesBaseForm
    template_name = 'esap/classes_ajax_form.html'


class ClassesCreateView(
    PermissionsRequiredMixin,
    AjaxableResponseMixin,
    generic.CreateView
):
    required_permissions = (
        'esap.add_classes',
    )
    template_name = 'esap/classes_form.html'
    model = Classes
    form_class = ClassesForm

    def get_success_url(self):
        return reverse('dashboard:classes_detail', kwargs={'pk': self.object.pk})


class ClassesDetailView(PermissionsRequiredMixin, generic.DetailView):
    required_permissions = (
        'esap.view_classes',
    )
    model = Classes

    def get_context_data(self, **kwargs):
        context = super(ClassesDetailView, self).get_context_data(**kwargs)
        context['materials'] = SupportMaterial.objects.filter(classes__exact=self.object.pk)
        return context


class ClassesAjaxDetailView(PermissionsRequiredMixin, generic.DetailView):
    """ """
    required_permissions = (
        'esap.view_classes',
    )
    template_name = 'esap/classes_list_row.html'
    model = Classes


class ClassesUpdateView(PermissionsRequiredMixin, UpdateWithInlinesView):
    required_permissions = (
        'esap.add_classes',
    )
    model = Classes
    form_class = ClassesForm
    inlines = [SupportMaterialFormSet, ]

    def get_success_url(self):
        return reverse('dashboard:classes_detail', kwargs={'pk': self.object.pk})


class ClassesAjaxUpdateView(
    PermissionsRequiredMixin,
    AjaxableResponseMixin,
    generic.UpdateView
):
    required_permissions = (
        'esap.add_classes',
    )
    model = Classes
    form_class = ClassesAjaxUpdateForm

    def get_success_url(self):
        return reverse('dashboard:classes_detail', kwargs={'pk': self.object.pk})


# Keywords

class KeywordCreateView(
    PermissionsRequiredMixin,
    AjaxableResponseMixin,
    generic.CreateView
):
    required_permissions = (
        'esap.add_keyword',
    )
    model = Keyword
    form_class = KeywordForm
    success_url = reverse_lazy('dashboard:keywords')
    template_name = 'esap/keyword_list.html'

    def get_context_data(self, **kwargs):
        context = super(KeywordCreateView, self).get_context_data(**kwargs)
        context['object_list'] = Keyword.objects.all()
        return context


class KeywordUpdateView(
    PermissionsRequiredMixin,
    generic.UpdateView
):
    required_permissions = (
        'esap.add_keyword',
    )
    model = Keyword
    form_class = KeywordForm
    success_url = reverse_lazy('dashboard:keywords')


class KeywordDetailView(
    PermissionsRequiredMixin,
    generic.DetailView
):
    required_permissions = (
        'keyword.view_keyword',
    )
    model = Keyword


# Plans

class PlanFormSet(InlineFormSet):
    model = Plan
    form_class = PlanForm
    extra = 1


# Modules

class ModuleListView(PermissionsRequiredMixin, generic.ListView):
    required_permissions = (
        'esap.view_module',
    )
    model = Module
    paginate_by = 10


class ModuleCreateAjaxFormView(PermissionsRequiredMixin, generic.FormView):
    required_permissions = (
        'esap.add_module',
    )
    form_class = ModuleBaseForm
    template_name = 'esap/modules_ajax_form.html'


class ModuleCreateView(
    PermissionsRequiredMixin,
    AjaxableResponseMixin,
    generic.CreateView
):
    required_permissions = (
        'esap.add_module',
    )
    template_name = 'esap/module_form.html'
    model = Module
    form_class = ModuleForm

    def get_success_url(self):
        return reverse('dashboard:modules_ajax_detail', kwargs={'pk': self.object.pk})


class ModuleAjaxDetailView(PermissionsRequiredMixin, generic.DetailView):
    """ """
    required_permissions = (
        'esap.view_module',
    )
    template_name = 'esap/modules_list_row.html'
    model = Module


class ModuleDetailView(
    PermissionsRequiredMixin,
    generic.DetailView
):
    required_permissions = (
        'esap.view_module',
    )
    model = Module


class ModuleUpdateView(PermissionsRequiredMixin, UpdateWithInlinesView):
    required_permissions = (
        'esap.add_module',
    )
    model = Module
    form_class = ModuleForm
    inlines = [PlanFormSet, ]

    def get_success_url(self):
        return reverse('dashboard:module_detail', kwargs={'pk': self.object.pk})


class ModuleAjaxUpdateView(
    PermissionsRequiredMixin,
    AjaxableResponseMixin,
    generic.UpdateView
):
    required_permissions = (
        'esap.add_module',
    )
    model = Module
    form_class = ModuleAjaxUpdateForm

    def get_success_url(self):
        return reverse('dashboard:module_detail', kwargs={'pk': self.object.pk})


# Instructors

class InstructorListView(PermissionsRequiredMixin, generic.ListView):
    required_permissions = (
        'esap.view_instructor',
    )
    model = Instructor


class InstructorCreateView(PermissionsRequiredMixin, generic.CreateView):
    required_permissions = (
        'esap.add_instructor',
    )
    model = Instructor
    form_class = InstructorForm

    def get_success_url(self):
        return reverse('dashboard:instructor_detail', kwargs={'pk': self.object.pk})


class InstructorUpdateView(PermissionsRequiredMixin, generic.UpdateView):
    required_permissions = (
        'esap.add_instructor',
    )
    model = Instructor
    form_class = InstructorForm

    def get_success_url(self):
        return reverse('dashboard:instructor_detail', kwargs={'pk': self.object.pk})


class InstructorDetailView(PermissionsRequiredMixin, generic.DetailView):
    required_permissions = (
        "esap.view_instructor",
    )
    model = Instructor


# Particular Clients

class ParticularClientListView(PermissionsRequiredMixin, generic.ListView):
    required_permissions = (
        'esap.view_particularclient',
    )
    model = ParticularClient


class ParticularClientCreateView(PermissionsRequiredMixin, generic.CreateView):
    required_permissions = (
        'esap.add_particularclient',
    )
    model = ParticularClient
    form_class = ParticularClientForm

    def get_success_url(self):
        return reverse('dashboard:particularclient_detail', kwargs={'pk': self.object.pk})


class ParticularClientUpdateView(PermissionsRequiredMixin, generic.UpdateView):
    required_permissions = (
        'esap.add_particularclient',
    )
    model = ParticularClient
    form_class = ParticularClientForm

    def get_success_url(self):
        return reverse('dashboard:particularclient_detail', kwargs={'pk': self.object.pk})


class ParticularClientDetailView(PermissionsRequiredMixin, generic.DetailView):
    required_permissions = (
        "esap.view_particularclient",
    )
    model = ParticularClient


class ParticularClientFullNameJsonView(
    PermissionsRequiredMixin,
    JSONResponseMixin,
    generic.DetailView
):
    required_permissions = (
        'esap.add_particularclient',
    )
    model = get_user_model()

    def options(self, request, *args, **kwargs):
        response = super(ParticularClientFullNameJsonView, self).options(request, *args, **kwargs)
        response['Content-type'] = "application/json"
        return response

    def get_data(self, context):
        context = {'fullname': context['object'].get_full_name()}
        return context

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)
