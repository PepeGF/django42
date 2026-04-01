# Training Django - Exercises (6.3-Sessions)

Proyecto de ejemplo que implementa los ejercicios del PDF `en.subject.pdf`.

## Requisitos
- Python 3
- Django 4.2 (ya configurado en el entorno virtual del workspace)

## Instalación rápida

Desde la carpeta `6.3-Sessions` y con el entorno virtual activado:

```bash
# activar venv (Windows ejemplo ya usado en este workspace)
d:/Docs/42/django42/django-venv/Scripts/activate
pip install -r requirements.txt   # si existe
# o instalar Django en el venv
pip install "django>=4.2,<4.3"

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Accede a http://127.0.0.1:8000/ para ver la página principal y a `/admin/` para administrar.

## Tests

Ejecutar los tests del ejercicio:

```bash
python manage.py test ex.tests
```

## Estructura relevante

- `ex/` - app con modelos, vistas, formularios, templates y tests.
- `ex/models.py` - `User` (custom con `reputation`), `Tip`, `Vote`.
- `ex/views.py` - homepage, creación de tips, voto, borrado, registro/login/logout.
- `ex/middleware.py` - middleware de sesión anónima (nombre válido 42s).
- `ex/templates/ex/` - templates `base.html`, `home.html`, `login.html`, `register.html`.
- `ex/tests.py` - tests unitarios para creación, voto, toggle, permisos y reputación.

## Pasos que seguí (resumen)

1. Convertí `6.3-Sessions/en.subject.pdf` a `en.subject.txt` y extraje requisitos.
2. Scaffold del proyecto Django en `6.3-Sessions` (`manage.py`, `ex_project/`).
3. Creé la app `ex` y la registré en `INSTALLED_APPS`.
4. Implementé modelos: `User` (custom con `reputation`), `Tip`, `Vote`.
5. Implementé `forms.py` con `TipForm` (ModelForm).
6. Implementé vistas: home (list + create), `vote`, `delete_tip`, `register`, `login`, `logout`.
7. Añadí `AnonymousSessionMiddleware` que asigna un nombre anónimo válido 42s.
8. Implementé señales para actualizar `reputation` al crear/actualizar/borrar votos y al borrar tips.
9. Añadí templates base y páginas de ejercicio (`home`, `login`, `register`).
10. Generé y apliqué migraciones, creé superuser de prueba y verifiqué el servidor.
11. Escribí tests en `ex/tests.py` que cubren creación de tips, votación (toggle), permisos y reputación.
12. Ejecuté `manage.py test` y ajusté código hasta que todos los tests pasaron.

## Siguientes pasos recomendados

- Mejorar la interfaz (Bootstrap), mensajes de usuario y validaciones UX.
- Añadir pruebas adicionales (autenticación, middleware, edge cases).
- Preparar README de entrega y empaquetado para la evaluación si hace falta.

---

Si quieres, puedo: (A) añadir Bootstrap y pulir templates, (B) ampliar la cobertura de tests, o (C) preparar un ZIP/PR listo para entrega.
