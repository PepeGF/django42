from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def index(request: HttpRequest) -> HttpResponse:
    return render(request, template_name='ex/base.html')