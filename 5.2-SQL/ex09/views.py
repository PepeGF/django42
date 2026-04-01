from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import F
from .models import People, Planets

def display(request: HttpRequest):
    qs = (
        People.objects
        .filter(homeworld__climate__icontains="windy")
        .select_related("homeworld")
        .order_by("name")
        .values(
            "name",
            homeworld_name=F("homeworld__name"),
            climate=F("homeworld__climate"),
        )
    )
    if not qs.exists():
        return HttpResponse("No data available, please use the following command line before use:" + \
                            "<br>python3 manage.py loaddata ex09_initial_data.json")
    return render(request, 'ex09/display.html', {'results': qs})