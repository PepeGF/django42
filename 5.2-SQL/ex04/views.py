from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest
from django.conf import settings
import psycopg2


def init(request: HttpRequest):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex04_movies (
                title VARCHAR(64) UNIQUE NOT NULL,
                episode_nb INTEGER PRIMARY KEY,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    return HttpResponse("OK")

def populate(request: HttpRequest):
    movies = movies_list()
    updated_movies = []
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        cur = conn.cursor()
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    for movie in movies:
        try:
            cur.execute("""
                INSERT INTO ex04_movies (title, episode_nb, opening_crawl, director, producer, release_date)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                movie["title"],
                movie["episode_nb"],
                movie["opening_crawl"],
                movie["director"],
                movie["producer"],
                movie["release_date"]
            ))
            updated_movies.append("OK")
            conn.commit()
        except Exception as e:
            updated_movies.append(movie["title"] + ": " + str(e))
            conn.rollback()
    cur.close()
    conn.close()
    return HttpResponse("<br>".join(updated_movies))

def display(request: HttpRequest):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ex04_movies;")
        movies = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    if not movies:
        return HttpResponse("No data available")
    return render(request, "ex04/display.html", {"movies": movies})

def remove(request: HttpRequest):
    try:
        conn = connect_db()
        cur = conn.cursor()
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    if request.method == "POST":
        movie_title = request.POST.get("movie")
        try:
            cur.execute("DELETE FROM ex04_movies WHERE title = %s;", (movie_title,))
            conn.commit()
        except Exception as e:
            return HttpResponse(f"Error: {e}")
        return redirect("ex04_remove")
    try:
        cur.execute("SELECT * FROM ex04_movies order by episode_nb;")
        movies = cur.fetchall()
        cur.close()
        conn.close()
        if len(movies) == 0:
            return HttpResponse("No data available")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    return render(request, "ex04/remove.html", {"movies": movies})

def connect_db() -> psycopg2.extensions.connection:
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def movies_list() -> list[dict]:
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