from django.shortcuts import render
from django.http import HttpResponse
from .models import Movies
import psycopg2
from django.conf import settings


def init(request):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex00_movies (
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