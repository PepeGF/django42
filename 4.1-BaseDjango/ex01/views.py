from django.shortcuts import render

# Create your views here.

def django(request):
    return render(request, 'ex01/django.html')

def display(request):
    return render(request, 'ex01/display.html')

def templatess(request):
    return render(request, 'ex01/templatess.html')