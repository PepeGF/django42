import os, json, random
from datetime import datetime, timedelta, timezone

# Create directories
os.makedirs('ex/fixtures', exist_ok=True)
os.makedirs('scripts', exist_ok=True)

# Deterministic timestamps
now = datetime(2026, 4, 3, 9, 0, 0, tzinfo=timezone.utc)

def iso(dt):
    return dt.isoformat().replace('+00:00', 'Z')

# Placeholder passwords (will be overwritten by script-generated hashes)
placeholder_hash = 'pbkdf2_sha256$600000$REEMPLAZA$REEMPLAZA'

users = [
    {
        "model": "auth.user",
        "pk": 1,
        "fields": {
            "password": placeholder_hash,
            "last_login": None,
            "is_superuser": False,
            "username": "djangouser",
            "first_name": "",
            "last_name": "",
            "email": "djangouser@example.com",
            "is_staff": False,
            "is_active": True,
            "date_joined": iso(now),
            "groups": [],
            "user_permissions": []
        }
    },
    {
        "model": "auth.user",
        "pk": 2,
        "fields": {
            "password": placeholder_hash,
            "last_login": None,
            "is_superuser": False,
            "username": "batman",
            "first_name": "",
            "last_name": "",
            "email": "batman@example.com",
            "is_staff": False,
            "is_active": True,
            "date_joined": iso(now),
            "groups": [],
            "user_permissions": []
        }
    },
    {
        "model": "auth.user",
        "pk": 3,
        "fields": {
            "password": placeholder_hash,
            "last_login": None,
            "is_superuser": False,
            "username": "bob",
            "first_name": "",
            "last_name": "",
            "email": "bob@example.com",
            "is_staff": False,
            "is_active": True,
            "date_joined": iso(now),
            "groups": [],
            "user_permissions": []
        }
    }
]

articles = []
article_data = [
    (1, "my story", 1, now - timedelta(days=3, hours=1), "The story of djangouser (this synopsis is deliberately longer than twenty chars).",
     "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n\nThis content can be anything."),
    (2, "POUET", 2, now - timedelta(days=8, hours=4), "POUET POUET", "Lorem ipsum."),
    (3, "I'm BATMAN", 2, now - timedelta(days=9, hours=2), "I'm REALLY BATMAN", "Lorem ipsum."),
    (4, "Bob l'éponge: La revanche de Plankton", 3, now - timedelta(days=10, hours=6),
     "Plankton a volé un pâté de crabe, Bob pourra-t-il sauver la situation. Attention, scènes de violence.",
     "Lorem ipsum."),
    (5, "Insanity", 2, now - timedelta(days=12, hours=1),
     "After leaving the Joker for the last time, Harley tries to rebuild her life away from Gotham and the Joker...",
     "Lorem ipsum."),
]
for pk, title, author_pk, created_dt, synopsis, content in article_data:
    articles.append({
        "model": "ex.article",
        "pk": pk,
        "fields": {
            "title": title,
            "author": author_pk,
            "created": iso(created_dt),
            "synopsis": synopsis,
            "content": content
        }
    })

favourites = [
    {"model": "ex.userfavouritearticle", "pk": 1, "fields": {"user": 1, "article": 2}},
    {"model": "ex.userfavouritearticle", "pk": 2, "fields": {"user": 1, "article": 3}},
]

fixture = users + articles + favourites
fixture_path = 'ex/fixtures/initial_data.json'
with open(fixture_path, 'w', encoding='utf-8') as f:
    json.dump(fixture, f, ensure_ascii=False, indent=2)

# Script to generate the same fixture but with real hashed passwords
script = r'''#!/usr/bin/env python3
"""Genera un fixture JSON con usuarios (password hasheada), artículos y favoritos.

Uso recomendado (desde la raíz del proyecto donde está manage.py):
  python scripts/generate_fixtures.py --settings Advance.settings --out ex/fixtures/initial_data.json

Luego cargar:
  python manage.py loaddata ex/fixtures/initial_data.json

Notas:
- No requiere que existan usuarios/artículos previos: el fixture los crea.
- Las contraseñas se hashean con el hasher de Django.
"""

import argparse
import json
import os
from datetime import datetime, timedelta, timezone


def iso(dt: datetime) -> str:
    return dt.isoformat().replace('+00:00', 'Z')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--settings', default=None, help='Módulo settings, ej: Advance.settings')
    ap.add_argument('--out', default='ex/fixtures/initial_data.json', help='Ruta de salida del fixture JSON')
    ap.add_argument('--password', default='1234', help='Password por defecto para los usuarios del ejemplo')
    args = ap.parse_args()

    if args.settings:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', args.settings)

    # Importar Django y preparar entorno
    import django
    django.setup()

    from django.contrib.auth.hashers import make_password

    now = datetime.now(timezone.utc)

    users = [
        {
            "model": "auth.user",
            "pk": 1,
            "fields": {
                "password": make_password(args.password),
                "last_login": None,
                "is_superuser": False,
                "username": "djangouser",
                "first_name": "",
                "last_name": "",
                "email": "djangouser@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": iso(now),
                "groups": [],
                "user_permissions": []
            }
        },
        {
            "model": "auth.user",
            "pk": 2,
            "fields": {
                "password": make_password(args.password),
                "last_login": None,
                "is_superuser": False,
                "username": "batman",
                "first_name": "",
                "last_name": "",
                "email": "batman@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": iso(now),
                "groups": [],
                "user_permissions": []
            }
        },
        {
            "model": "auth.user",
            "pk": 3,
            "fields": {
                "password": make_password(args.password),
                "last_login": None,
                "is_superuser": False,
                "username": "bob",
                "first_name": "",
                "last_name": "",
                "email": "bob@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": iso(now),
                "groups": [],
                "user_permissions": []
            }
        }
    ]

    article_data = [
        (1, "my story", 1, now - timedelta(days=3, hours=1), "The story of djangouser (this synopsis is deliberately longer than twenty chars).",
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n\nThis content can be anything."),
        (2, "POUET", 2, now - timedelta(days=8, hours=4), "POUET POUET", "Lorem ipsum."),
        (3, "I'm BATMAN", 2, now - timedelta(days=9, hours=2), "I'm REALLY BATMAN", "Lorem ipsum."),
        (4, "Bob l'éponge: La revanche de Plankton", 3, now - timedelta(days=10, hours=6),
         "Plankton a volé un pâté de crabe, Bob pourra-t-il sauver la situation. Attention, scènes de violence.",
         "Lorem ipsum."),
        (5, "Insanity", 2, now - timedelta(days=12, hours=1),
         "After leaving the Joker for the last time, Harley tries to rebuild her life away from Gotham and the Joker...",
         "Lorem ipsum."),
    ]

    articles = []
    for pk, title, author_pk, created_dt, synopsis, content in article_data:
        articles.append({
            "model": "ex.article",
            "pk": pk,
            "fields": {
                "title": title,
                "author": author_pk,
                "created": iso(created_dt),
                "synopsis": synopsis,
                "content": content
            }
        })

    favourites = [
        {"model": "ex.userfavouritearticle", "pk": 1, "fields": {"user": 1, "article": 2}},
        {"model": "ex.userfavouritearticle", "pk": 2, "fields": {"user": 1, "article": 3}},
    ]

    fixture = users + articles + favourites

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(fixture, f, ensure_ascii=False, indent=2)

    print(f"Fixture generado en: {args.out}")
    print(f"Usuarios: djangouser, batman, bob (password: {args.password})")


if __name__ == '__main__':
    main()
'''

script_path = 'scripts/generate_fixtures.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script)

# Make script executable (best effort)
try:
    os.chmod(script_path, 0o755)
except Exception:
    pass

# Return paths
(fixture_path, script_path)