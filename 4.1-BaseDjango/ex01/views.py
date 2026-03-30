from django.shortcuts import render


def django_page(request):
    """Render a brief introduction to Django and its history."""
    return render(request, 'ex01/django.html')


def display_page(request):
    """Describe the process that displays a static page (template -> view -> response)."""
    return render(request, 'ex01/display.html')


def templates_page(request):
    """Show how the Django template engine works with examples for blocks, loops and ifs.

    Pass example context to demonstrate variable display and looping.
    """
    context = {
        'items': ['one', 'two', 'three'],
        'show_extra': True,
        'message': 'This is a context variable passed from the view.'
    }
    return render(request, 'ex01/templates.html', context)

def django(request):
    return render(request, 'ex01/django.html')

def display(request):
    return render(request, 'ex01/display.html')

def templatess(request):
    return render(request, 'ex01/templatess.html')