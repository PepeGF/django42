from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from .models import Movies
from .forms import UpdateForm

def populate(request: HttpRequest):
    movies = all_movies()
    added_movies = []
    for movie in movies:
        try:
            Movies.objects.create(
                title=movie["title"],
                episode_nb=movie["episode_nb"],
                opening_crawl=movie["opening_crawl"],
                director=movie["director"],
                producer=movie["producer"],
                release_date=movie["release_date"]
            )
            added_movies.append("OK")
        except Exception as e:
            added_movies.append(f"Error inserting {movie['title']}: {e}")
    return HttpResponse("<br>".join(added_movies))

def display(request: HttpRequest):
    try:
        movies = Movies.objects.all().order_by('episode_nb')
    except Exception as e:
        return HttpResponse(f"Error retrieving movies: {e}")
    if len(movies) == 0:
        return HttpResponse("No data available")
    return render(request, 'ex07/display.html', {"movies": movies})

def update(request: HttpRequest):
    # Get all movies for the dropdown
    try:
        movies = Movies.objects.all().order_by('episode_nb')
    except Exception as e:
        return HttpResponse(f"Error retrieving movies: {e}")
    if len(movies) == 0:
        return HttpResponse("No data available")
    choices = [(movie.episode_nb, movie.title) for movie in movies]
    if request.method == "POST":
        form = UpdateForm(choices, request.POST)
        if form.is_valid():
            nb = int(form.cleaned_data['movie'])
            new_crawl = form.cleaned_data['opening_crawl'] or None
            try:
                movie_to_update = Movies.objects.get(episode_nb=nb)
                movie_to_update.opening_crawl = new_crawl
                movie_to_update.save()
                return redirect("ex07_display")
            except Exception as e:
                return HttpResponse(f"Error updating movie: {e}")
    else:
        form = UpdateForm(choices)
    return render(request, 'ex07/update.html', {"movies": movies, "form": form})

def all_movies() -> list[dict]:
    return [
        {
            "title": "The Phantom Menace",
            "episode_nb": 1,
            "opening_crawl": None,
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19"
        },
        {
            "title": "Attack of the Clones",
            "episode_nb": 2,
            "opening_crawl": None,
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16"
        },
        {
            "title": "Revenge of the Sith",
            "episode_nb": 3,
            "opening_crawl": None,
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19"
        },
        {
            "title": "A New Hope",
            "episode_nb": 4,
            "opening_crawl": None,
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25"
        },
        {
            "title": "The Empire Strikes Back",
            "episode_nb": 5,
            "opening_crawl": None,
            "director": "Irvin Kershner",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1980-05-17"
        },
        {
            "title": "Return of the Jedi",
            "episode_nb": 6,
            "opening_crawl": None,
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25"
        },
        {
            "title": "The Force Awakens",
            "episode_nb": 7,
            "opening_crawl": None,
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11"
        }
    ]