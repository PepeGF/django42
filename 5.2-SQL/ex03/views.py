from django.shortcuts import render
from django.http import HttpResponse
from django import db
from .models import Movies
# Create your views here.

def populate(request):
    movies = [
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
    inserted_movies = []
    # for movie_data in movies:
    #     try:
    #         movie = Movies(**movie_data)
    #         movie.save()
    #         inserted_movies.append("OK")
    #     except Exception as e:
    #         inserted_movies.append(str(e))
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
            inserted_movies.append("OK")
        except db.Error as e:
            inserted_movies.append(str(e))
    return HttpResponse("<br>".join(inserted_movies))

def display(request):
    try:
        movies = Movies.objects.all()
        if len(movies) == 0:
            return HttpResponse("No data available")
    except db.Error as e:
        return HttpResponse(f"Error: {e}")
    return render(request, 'ex03/display.html', {'movies': movies})