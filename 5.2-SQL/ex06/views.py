from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from .forms import UpdateForm
import psycopg2


def init(request: HttpRequest):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        cur = conn.cursor()
        table_name = "ex06_movies"
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                title VARCHAR(64) UNIQUE NOT NULL,
                episode_nb INTEGER PRIMARY KEY,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        
            CREATE OR REPLACE FUNCTION update_changetimestamp_column()
            RETURNS TRIGGER AS $$
            BEGIN
            NEW.updated = now();
            NEW.created = OLD.created;
            RETURN NEW;
            END;
            $$ language 'plpgsql';
            CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
            ON {table_name} FOR EACH ROW EXECUTE PROCEDURE
            update_changetimestamp_column();
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    return HttpResponse("OK")

def populate(request: HttpRequest):
    movies = all_movies()
    updated_movies = []
    try:
        conn = connect_db()
        if conn is None:
            raise Exception("Could not connect to the database")
        cur = conn.cursor()
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    for movie in movies:
        try:
            cur.execute("""
                INSERT INTO ex06_movies (title, episode_nb, opening_crawl, director, producer, release_date)
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
        if conn is None:
            raise Exception("Could not connect to the database")
        cur = conn.cursor()
        cur.execute("SELECT * FROM ex06_movies order by episode_nb;")
        movies = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    if not movies:
        return HttpResponse("No data available")
    return render(request, "ex06/display.html", {"movies": movies})

def update(request: HttpRequest):
    conn = connect_db()
    if conn is None:
        return HttpResponse("DB connection error")
    cur = conn.cursor()
    try:
        cur.execute("SELECT episode_nb, title FROM ex06_movies ORDER BY episode_nb;")
        rows = cur.fetchall()
        if not rows:
            return HttpResponse("No data available")
        choices = [(str(r[0]), r[1]) for r in rows]

        if request.method == "POST":
            form = UpdateForm(choices, request.POST)
            if form.is_valid():
                nb = int(form.cleaned_data['movie'])
                new_crawl = form.cleaned_data['opening_crawl'] or None
                try:
                    cur.execute(
                        f"UPDATE ex06_movies SET opening_crawl = {new_crawl} WHERE episode_nb = {nb};"
                    )
                    conn.commit()
                    return redirect("ex06_display")
                except Exception as e:
                    conn.rollback()
                    return HttpResponse(f"Error: {e}")
        else:
            form = UpdateForm(choices)
        return render(request, "ex06/update.html", {"form": form})
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass

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

def all_movies():
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

