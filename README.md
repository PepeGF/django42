# django42
Piscina Django 42

Revisando nav.html, rutas y plantillas para asegurar el selector y traducciones están en su lugar. Luego ajustaré cualquier plantilla o URL que falte.

Voy a marcar todas las cadenas relevantes para traducción y añadir el selector de idioma en nav.html. Esto actualizará base.html, nav.html y las plantillas de ex/ para que respeten el prefijo de idioma.

He implementado la internacionalización necesaria y añadí un borrador de traducciones en español.

Cambios realizados (relevantes)

Advance/settings.py: activado LocaleMiddleware, añadido django.template.context_processors.i18n, configurado LANGUAGES y LOCALE_PATHS.
Advance/urls.py: rutas envueltas con i18n_patterns(...) y añadido path('i18n/', ...) para exponer set_language (por eso ahora /en/... y /es/... funcionan).
ex/templates/*: marqué las cadenas para traducción y añadí selector de idioma en ex/templates/nav.html.
Afectadas: base.html, nav.html, ex/article_list.html, ex/publications.html, ex/article_detail.html, ex/login.html, ex/logout.html, ex/favourite.html, ex/register.html, ex/publish.html.
Creé un borrador de traducciones: locale/es/LC_MESSAGES/django.po (con las cadenas usadas por la funcionalidad de Articles y el menú).
Qué comprobar y cómo probar localmente

Reinicia el servidor:
Prueba las URLs con prefijo de idioma:
http://127.0.0.1:8000/en/articles → contenido en inglés
http://127.0.0.1:8000/es/articles → contenido en español
Cambiar idioma desde la página:
En la barra de navegación verás un selector de idioma; al cambiarlo hace POST a set_language y la página usará el idioma seleccionado.
Generar/compilar traducciones (en tu máquina)

Si quieres actualizar/extraer automáticamente cadenas:
python manage.py makemessages -l es
Edita locale/es/LC_MESSAGES/django.po (ya existe un borrador que creé).
Compila los mensajes:
python manage.py compilemessages
Nota: compilemessages necesita gettext/msgfmt instalado (en Windows instala gettext o usa WSL).

Estado respecto a los requisitos del ejercicio

La URL por defecto incluirá el prefijo en si navegas con ese prefijo (porque las rutas usan i18n_patterns, que por defecto añade el prefijo).
Hay un selector de idioma en las páginas (en el menú) que permite cambiar el idioma.
Las plantillas de la funcionalidad Articles (menú, encabezados de tabla, botones, mensajes) están marcadas para traducción y tienen entradas en locale/es/... (borrador).