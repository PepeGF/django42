from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import Prefetch
from .models import Planets, People, Movies
from .forms import FilterForm

def display(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        warning_text = "Nothing corresponding to your search"
    else:
        warning_text = "Please fill the form to display results"
    genders = People.objects.values_list('gender', flat=True).distinct()
    gender_choices = [(g, g.title()) for g in genders if g not in ('none','', 'n/a', None)]
    form = FilterForm(gender_choices=gender_choices)
    movies = []
    form = FilterForm(gender_choices=gender_choices, data=request.POST)
    if form.is_valid():
        min_date = form.cleaned_data['min_release_date']
        max_date = form.cleaned_data['max_release_date']
        diameter_gt = form.cleaned_data['diameter_gt']
        gender = form.cleaned_data['gender']

        people_qs = (
            People.objects
            .filter(gender=gender, homeworld__diameter__gte=diameter_gt)
            .select_related('homeworld')
            .order_by('name')
        )
        movies_qs = (
            Movies.objects
            .filter(release_date__gte=min_date, release_date__lte=max_date)
            .prefetch_related(Prefetch('characters', queryset=people_qs))
            .order_by('release_date')
        )
        for movie in movies_qs:
            for person in movie.characters.all():
                hw = person.homeworld
                movies.append({
                    'movie_name': movie.title,
                    'character_name': person.name,
                    'character_gender': person.gender,
                    'character_homeworld': hw.name if hw else None,
                    'planet_diameter': hw.diameter if hw else None,
                })
    return render(
        request,
        'ex10/display.html', 
        {
            'movies': movies, 
            'form': form, 
            'warning_text': warning_text
            }
    )