# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import logout as logout_user, login as login_user, authenticate
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from .forms import RegistrationForm, LoginForm
from .models import User


def register(request, template_name='account/register.html'):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            email = cleaned_data.get('email', None)
            first_name = cleaned_data.get('first_name', None)
            last_name = cleaned_data.get('last_name', None)
            birthday = cleaned_data.get('birthday', None)
            password = cleaned_data.get('password', None)
            user = User.objects.create_user(email, first_name, last_name, birthday, password)
            user.save()
            user = authenticate(username=email, password=password)
            login_user(request, user)
            messages.success(request, "Bem vindo! Você foi cadastrado com sucesso!")
            return redirect(request.POST.get('next', reverse("dashboard:home")))
    else:
        initial = {'email': request.GET.get('email', None)}
        form = RegistrationForm(initial=initial)
    context = {'form': form, 'next': request.GET.get('next', None), }
    return render_to_response(template_name, context, RequestContext(request))


def registration_successful(request, template_name='account/registration_successful.html'):
    return render_to_response(template_name, RequestContext(request))


def profile(request, template_name='account/profile.html'):
    return render_to_response(template_name, RequestContext(request))


def activate(request, template_name='account/activate.html'):
    form = RegistrationForm()
    return render_to_response(template_name, {'form': form, }, RequestContext(request))


def login(request, template_name='account/login.html'):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.login(request):
            messages.success(request, "Você efetuou login com sucesso!")
            return redirect(request.GET.get('next', reverse("dashboard:home")))
        else:
            messages.error(request, "Email e/ou senha inválidos.")
    else:
        form = LoginForm()
    return render_to_response(template_name, {'form': form, }, RequestContext(request))


def logout(request):
    logout_user(request)
    messages.success(request, "Deslogado com sucesso. Volte sempre!")
    return redirect('home')


def manage(request, template_name='account/manage.html'):
    return render_to_response(template_name, {}, RequestContext(request))
