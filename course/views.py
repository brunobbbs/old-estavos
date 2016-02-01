# -*- coding: utf-8 -*-
from django.views import generic

from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from utils.ajax import AjaxableResponseMixin
from extra_views import CreateWithInlinesView, InlineFormSet
from pagseguro.api import PagSeguroItem, PagSeguroApi
from portal.models import CourseLead
from .models import Subscription, Student
from .forms import CourseSubscriptionForm, StudentForm, CourseLeadForm


class StudentFormSet(InlineFormSet):
    model = Student
    form_class = StudentForm
    extra = 1

    def get_factory_kwargs(self):
        kwargs = super(StudentFormSet, self).get_factory_kwargs()
        kwargs.update({
            "min_num": 1,
            "validate_min": True
        })
        return kwargs


class CourseCheckoutView(generic.TemplateView):

    template_name = "course/checkout.html"

    def get_context_data(self, **kwargs):
        kwargs = super(CourseCheckoutView, self).get_context_data(**kwargs)

        user_id = self.request.session.get("user_subscription", "")
        if user_id:
            obj = get_object_or_404(Subscription, pk=user_id)
            if not obj.students.count():
                student = Student.objects.create(name=obj.name, age=0, subscription=obj)
                student.save()
            course_price = obj.course.price
            qtd = obj.students.count()
            total = qtd * course_price
            kwargs.update(subscription=obj, total=total)
        else:
            raise Http404

        return kwargs


class CourseSubscriptionView(CreateWithInlinesView):

    def __init__(self, *args, **kwargs):
        super(CourseSubscriptionView, self).__init__(*args, **kwargs)
        for form in self.inlines:
            form.empty_permitted = False

    model = Subscription
    form_class = CourseSubscriptionForm

    inlines = [StudentFormSet, ]

    def get_success_url(self):
        self.request.session['user_subscription'] = self.object.pk
        self.request.session.set_expiry(0)
        return reverse('course:checkout')

    def form_valid(self, form):
        form.subscription_alert()
        form.client_subscription_mail()
        return super(CourseSubscriptionView, self).form_valid(form)


class CourseView(SuccessMessageMixin, generic.CreateView):
    """ """
    template_name = "course/course.html"
    model = CourseLead
    form_class = CourseLeadForm
    success_message = "Recebemos seus dados. Entraremos em contato assim que tivermos novas turmas. Obrigado!"

    def get_success_url(self):
        return reverse("course:index")


class CoursePagseguroReturn(generic.TemplateView):

    template_name = "course/pagseguro_return.html"
    subscription = None

    def get_subscription(self):
        if self.subscription:
            return self.subscription
        else:
            subscription = self.request.session.get("user_subscription", "")
            obj = get_object_or_404(Subscription, pk=subscription)
            self.subscription = obj
        return obj

    def get_data(self, code):
        if not code:
            return
        pg = PagSeguroApi()
        data = pg.get_transaction(code)
        if data['success']:
            self.update_transaction_status(data['transaction']['status'])
            return data
        return {}

    def update_transaction_status(self, code):
        obj = self.get_subscription()
        obj.status = code
        obj.save()
        return

    def get_context_data(self, **kwargs):
        kwargs = super(CoursePagseguroReturn, self).get_context_data(**kwargs)
        code = self.request.GET.get("cod", "")
        obj = self.get_subscription()
        if not code:
            raise Http404
        kwargs.update({'subscription': obj})
        if not obj.transaction:
            obj.transaction = code
            obj.save()
        data = self.get_data(code)
        if data:
            kwargs.update(data)
        return kwargs


class PagseguroPayment(generic.RedirectView):

    def pagseguro(self, subscription):
        obj = get_object_or_404(Subscription, pk=subscription)
        item = PagSeguroItem(
            id=obj.course.pk,
            description=obj.course.name,
            amount=obj.course.price,
            quantity=obj.students.count()
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
            return reverse("course:checkout")

    def get_redirect_url(self, *args, **kwargs):
        subscription = self.request.session.get("user_subscription", "")
        if not subscription:
            return reverse("course:subscription")
        url = self.pagseguro(subscription)
        return url
