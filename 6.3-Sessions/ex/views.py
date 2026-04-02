from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import RegistrationForm, LoginForm, TipForm
from .models import Tips
import random


def index(request: HttpRequest) -> HttpResponse:
    tips = Tips.objects.all()
    form = TipForm()
    return render(
        request, 
        template_name='ex/index.html', 
        context={'tips': tips, 'form': form})

def register(request: HttpRequest) -> HttpResponse:
    # Placeholder for registration logic
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['user_name'],
                password=form.cleaned_data['password']
            )
            user = authenticate(
                request, 
                username=form.cleaned_data['user_name'], 
                password=form.cleaned_data['password']
            )
            if user:
                auth_login(request, user)
                return redirect('index')
        else:
            print(f"Form errors: {form.errors}")

    else:
        form = RegistrationForm()
    return render(request, template_name='ex/register.html', context={'form': form})

def login(request: HttpRequest) -> HttpResponse:
    # Placeholder for login logic
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, template_name='ex/login.html', context={'form': form})

def logout(request: HttpRequest) -> HttpResponse:
    auth_logout(request)
    return redirect('index')

def nav_text(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        text = request.user.get_username()
        authenticated = True
    else:
        text = random.choice(settings.RANDOM_NAMES)
        authenticated = False
    return JsonResponse({'random_name': text, 'authenticated': authenticated})

@login_required
def add_tip(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TipForm(request.POST)
        if form.is_valid():
            post: Tips = form.save(commit=False)
            post.author = request.user.get_username()
            post.save()
            return redirect('index')
    else:
        form = TipForm()
    return redirect('index')