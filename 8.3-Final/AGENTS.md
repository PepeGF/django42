# Django 08 - Final: AJAX Login + Chat con WebSockets

## Reglas generales

- Máquina virtual con todo el software necesario configurado e instalado.
- Carpeta compartida entre VM y host para evaluaciones.
- Las funciones no deben fallar inesperadamente.
- Usar **Python3** y **Django** (versión LTS recomendada).
- Entregar un `requirements.txt` generado con `pip freeze`.
- Dejar la **aplicación de administración por defecto activada** (`django.contrib.admin`).

## Reglas específicas del día — MUY IMPORTANTES

1. **La única librería JavaScript permitida es JQuery**. No React, no Vue, no Angular, no otra cosa. Solo JQuery.
2. **Un solo proyecto Django** llamado `d09`. No se divide en carpetas de ejercicios separadas. Cada ejercicio AÑADE funcionalidad al mismo proyecto.
3. **Dejar la aplicación de administración por defecto activada.**
4. **Entregar `requirements.txt`** con `pip freeze`.
5. **WebSockets** para el chat (ejercicios 01-04). Usar **Django Channels** como backend de WebSockets.
6. **AJAX** (JQuery `$.ajax()` o `$.post()`) para el login/logout (ejercicio 00). Las peticiones AJAX deben ser de tipo **POST**.
7. **La página NUNCA debe refrescarse** en las interacciones AJAX/WebSocket (excepto refresh manual del usuario).
8. Se puede usar **Bootstrap** para CSS (opcional en ex00, recomendado para ex04).

## Estructura del proyecto

```
Django - 08 - Final/
├── manage.py
├── requirements.txt
├── Dockerfile
├── d09/                        # Proyecto Django principal
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py                 # IMPORTANTE: configurar para Channels (WebSockets)
├── account/                    # App para login/logout AJAX (ex00)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── forms.py
│   ├── migrations/
│   ├── templates/
│   │   └── account/
│   │       └── index.html      # Página principal de login/logout
│   └── static/
│       └── account/
│           └── js/
│               └── account.js  # JavaScript AJAX para login/logout
├── chat/                       # App para chat WebSocket (ex01-ex04)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # ChatRoom, ChatMessage
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── consumers.py            # WebSocket consumers (Django Channels)
│   ├── routing.py              # WebSocket URL routing
│   ├── migrations/
│   ├── templates/
│   │   └── chat/
│   │       ├── rooms.html      # Lista de chatrooms (3 links)
│   │       └── room.html       # Página del chatroom individual
│   └── static/
│       └── chat/
│           └── js/
│               └── chat.js     # JavaScript WebSocket para chat
```

---

## Configuración inicial

### Paso 1: Crear proyecto y apps

```bash
django-admin startproject d09 .
python manage.py startapp account
python manage.py startapp chat
```

### Paso 2: Instalar dependencias

```bash
pip install channels
pip freeze > requirements.txt
```

> **Nota sobre channels**: Django Channels añade soporte para WebSockets a Django. Para desarrollo/evaluación, se usa el **InMemoryChannelLayer** (sin necesidad de Redis ni Daphne). Funciona con el `runserver` estándar de Django.

### Paso 3: Configurar `d09/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'account',
    'chat',
]

# ASGI application
ASGI_APPLICATION = 'd09.asgi.application'

# Channel Layers - InMemoryChannelLayer para desarrollo:
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

LOGIN_URL = '/account/'
```

### Paso 4: Configurar `d09/asgi.py`

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd09.settings')

django_asgi_app = get_asgi_application()

from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
```

> **IMPORTANTE**: `AuthMiddlewareStack` permite que el WebSocket consumer acceda a `self.scope['user']` para saber qué usuario está conectado. Solo usuarios autenticados pueden usar el chat.

### Paso 5: Configurar `d09/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('chat/', include('chat.urls')),
]
```

### Paso 6: Crear superusuario

```bash
python manage.py createsuperuser
```

Crear al menos 2-3 usuarios de prueba (vía admin o `createsuperuser`).

### Paso 7: Ejecutar el servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## Exercise 00: Login with AJAX

**Objetivo**: Sistema de conexión/desconexión usando EXCLUSIVAMENTE AJAX (JQuery). La página NUNCA se refresca.

### URL

- `127.0.0.1:8000/account/` → Página principal de la app account

### Comportamiento (dos estados)

#### Estado 1: Usuario NO conectado
- La página muestra un **formulario estándar de login** (username + password).
- La comunicación con el servidor es **SOLO por AJAX** y de tipo **POST**.
- Si el formulario **no es válido**: los errores aparecen en la página **SIN refresco**.
- Si el formulario **es válido**: el formulario **desaparece** y la página adopta el Estado 2. **SIN refresco**.

#### Estado 2: Usuario conectado
- La página muestra el texto: `"Logged as <username>"` (reemplazar `<username>` por el nombre del usuario).
- Se muestra un botón **"Logout"**.
- El botón Logout comunica con el servidor vía **AJAX** y método **POST**.
- Al hacer logout: el texto y el botón desaparecen y la página vuelve al Estado 1. **SIN refresco**.

#### Comportamiento al refrescar
- Si se refresca manualmente la página, debe volver al estado correcto (si estaba logueado → Estado 2, si no → Estado 1).
- Los errores del formulario NO se mantienen tras refrescar.

### Modelo

No se necesitan modelos adicionales. Usar el modelo `User` de Django (`django.contrib.auth`).

### Vista (`account/views.py`)

```python
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views import View

# Vista para renderizar la página
class AccountView(TemplateView):
    template_name = 'account/index.html'

# Vista AJAX para login (POST)
# Recibe username y password, autentica, devuelve JSON
# Si éxito: {'success': True, 'username': user.username}
# Si error: {'success': False, 'errors': {'__all__': ['Invalid credentials']}}

# Vista AJAX para logout (POST)
# Desloguea al usuario, devuelve JSON
# {'success': True}
```

> **Nota**: Para el login AJAX se puede usar `AuthenticationForm` (mencionado en el subject: "AuthenticationForm, for free!"). El form se instancia en el servidor, se valida y se devuelve JSON.

> **IMPORTANTE sobre CSRF**: Las peticiones AJAX POST necesitan el token CSRF. En JQuery, obtener el token de la cookie `csrftoken` y añadirlo al header `X-CSRFToken`. Incluir `{% csrf_token %}` en el formulario HTML y leerlo desde ahí, o usar el patrón estándar de Django para AJAX:

```javascript
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
```

### Template (`account/templates/account/index.html`)

- Incluir **JQuery** (CDN).
- Formulario HTML con `id` para manipulación con JQuery.
- Div para errores.
- Div para el estado logueado ("Logged as..." + botón Logout).
- Renderizar el estado inicial según `{{ user.is_authenticated }}`.

### JavaScript (`account/static/account/js/account.js`)

- Al enviar el formulario de login: `$.ajax()` POST a la URL de login.
  - Si éxito: ocultar formulario, mostrar "Logged as ..." + Logout.
  - Si error: mostrar errores en el div de errores.
- Al hacer clic en Logout: `$.ajax()` POST a la URL de logout.
  - Si éxito: ocultar "Logged as..." y Logout, mostrar formulario de login.

### URLs (`account/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.AccountView.as_view(), name='index'),
    path('login/', views.LoginAjaxView.as_view(), name='login'),
    path('logout/', views.LogoutAjaxView.as_view(), name='logout'),
]
```

### Criterios de evaluación (de la corrección)

- [ ] Crear un usuario administrador con `./manage.py createsuperuser`
- [ ] La página NO se refresca por sí sola durante toda la evaluación
- [ ] Si no estás conectado, `127.0.0.1:8000/account/` muestra un formulario estándar de login
- [ ] Si llenas mal el formulario, aparecen errores
- [ ] Si llenas correctamente el formulario, desaparece y aparece un botón "Logout" con el texto "Logged as <username>"
- [ ] Cerrar la página y reabrirla: debes seguir logueado y el formulario de login NO debe aparecer
- [ ] Verificar que funciona como administrador conectándote al admin page (`/admin/`). No deberías tener que loguearte de nuevo
- [ ] Hacer clic en "Logout": el formulario debe reaparecer mientras el menú desaparece. Esta vez, volver a ir a la admin page. Esta vez, deberías tener que loguearte

---

## Exercise 01: Basic Chat with WebSockets

**Objetivo**: Crear un chat funcional usando WebSockets (NO AJAX). Solo JQuery como librería JS.

### Modelos (`chat/models.py`)

#### Modelo `ChatRoom`
| Campo  | Tipo                        | Restricciones |
|--------|-----------------------------|---------------|
| `name` | `CharField(max_length=100)` | Unique        |

- `__str__()` → `self.name`
- Los nombres de las salas deben estar en la base de datos (crear 3 salas).

#### Modelo `ChatMessage` (necesario para ex02 - historial)
| Campo      | Tipo                             | Restricciones                       |
|------------|----------------------------------|-------------------------------------|
| `room`     | `ForeignKey(ChatRoom)`           | `on_delete=CASCADE`                 |
| `user`     | `ForeignKey(User)`               | `on_delete=CASCADE`                 |
| `content`  | `TextField`                      | Non null                            |
| `timestamp`| `DateTimeField(auto_now_add=True)` | Auto                              |

- `__str__()` → algo descriptivo como `f"{self.user.username}: {self.content[:50]}"`

> **Nota**: Aunque `ChatMessage` se usa completamente en ex02, es mejor crear el modelo desde el principio para evitar migraciones posteriores complicadas.

### Vista de lista de salas (`chat/views.py`)

- URL para ver la **lista de 3 chatrooms** como 3 **links**.
- Cada link lleva a una URL de chatroom individual.
- **Solo accesible para usuarios conectados** (redirigir a login si no autenticado).

### Vista de chatroom individual

- URL con identificador de la sala (slug o pk).
- Muestra la página del chat.
- **Solo accesible para usuarios conectados**.

### WebSocket Consumer (`chat/consumers.py`)

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        # Rechazar si no autenticado
        if not self.user.is_authenticated:
            await self.close()
            return

        # Unirse al grupo del chatroom
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Enviar mensaje de que el usuario se unió
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user.username} has joined the chat',
                'username': 'system',
            }
        )

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Guardar mensaje en BD (para ex02)
        await self.save_message(message)

        # Enviar mensaje al grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
            }
        )

    async def chat_message(self, event):
        # Enviar mensaje al WebSocket del cliente
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

    @database_sync_to_async
    def save_message(self, message):
        from .models import ChatRoom, ChatMessage
        room = ChatRoom.objects.get(name=self.room_name)
        ChatMessage.objects.create(
            room=room,
            user=self.user,
            content=message,
        )
```

### WebSocket Routing (`chat/routing.py`)

```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
```

### URLs (`chat/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.RoomListView.as_view(), name='rooms'),
    path('<str:room_name>/', views.RoomView.as_view(), name='room'),
]
```

### Template del chatroom (`chat/templates/chat/room.html`)

- Incluir **JQuery** (CDN).
- Mostrar el **nombre del chatroom** en algún lugar visible.
- Div/contenedor para los **mensajes**.
- Input de texto + botón para **enviar mensaje**.
- Los mensajes aparecen en el fondo (**bottom**) y en **orden ascendente** (más antiguo arriba, más nuevo abajo).
- Cada mensaje muestra: `<username>: <message>`.

### JavaScript (`chat/static/chat/js/chat.js`)

```javascript
// Conexión WebSocket
const roomName = /* obtener nombre de sala del template */;
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

// Recibir mensaje
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // Añadir mensaje al contenedor de mensajes (al final/bottom)
    // Formato: "<username>: <message>" o "system: <username> has joined"
};

// Enviar mensaje
$('#send-btn').click(function() {
    const message = $('#message-input').val();
    chatSocket.send(JSON.stringify({ 'message': message }));
    $('#message-input').val('');
});
```

### Especificaciones del chat (CRÍTICAS para la corrección)

1. **Usa WebSockets** (NO AJAX) para la comunicación del chat.
2. **Solo accesible para usuarios conectados** (no se puede chatear sin login).
3. **El nombre del chatroom** aparece visible en la página.
4. **La página no se refresca sola** (no polling, no refresh automático).
5. **Varios usuarios pueden conectarse** a la misma sala.
6. **Un mensaje enviado es visible para TODOS** los usuarios de esa sala.
7. **Los mensajes aparecen abajo** (bottom), en orden ascendente (viejo arriba → nuevo abajo).
8. **Los mensajes NO desaparecen**. Un mensaje NO reemplaza al anterior. El orden NO cambia.
9. **Cuando un usuario se une**: aparece el mensaje `"<username> has joined the chat"` para TODOS (incluido él mismo).

### Datos iniciales

Crear **3 chatrooms** en la base de datos. Se pueden crear via:
- Admin de Django
- Fixture
- Migration con datos iniciales
- Shell: `python manage.py shell` → `ChatRoom.objects.create(name='room1')` etc.

### Criterios de evaluación (de la corrección)

- [ ] La dirección asignada al estudiante da acceso a la lista del chat
- [ ] Hay 3 links que llevan a 3 chatrooms diferentes
- [ ] Las 3 chatrooms se comportan como sigue:
  - [ ] El acceso es imposible sin estar logueado
  - [ ] La página no se refresca sola
  - [ ] El nombre del chatroom aparece en algún lugar
  - [ ] Se pueden enviar mensajes. Aparecen uno tras otro, de arriba abajo, con el nombre del usuario que los envió
  - [ ] Un mensaje no debe desaparecer ni ser reemplazado por otro. Si hay scrollbar, el mensaje debe ser accesible mediante ella
  - [ ] Loguearse con dos (o varios) usuarios diferentes en el mismo chatroom. El primero debe ver `"<username> has joined the chat"` con su propio username, y otro usuario con el username del otro
  - [ ] Cuando uno está logueado y el otro escribe un mensaje, todos los logueados en el chatroom pueden verlo
  - [ ] Conectar los usuarios a dos chatrooms diferentes y asegurarse de que esta vez uno no puede ver el mensaje del otro

---

## Exercise 02: Message History with WebSockets

**Objetivo**: Añadir historial de mensajes al chat. Al unirse a un chatroom, se muestran los últimos 3 mensajes.

### Implementación

1. **Guardar mensajes en BD**: Cada mensaje enviado se guarda en el modelo `ChatMessage` (ya implementado en el consumer de ex01).

2. **Al conectarse (en `connect()` del consumer)**: Después de aceptar la conexión y ANTES de enviar el mensaje "has joined the chat", enviar los **últimos 3 mensajes** de ese chatroom al usuario que se conecta.

3. **Los 3 mensajes del historial** aparecen **de arriba abajo, del más antiguo al más reciente**.

### Modificar el Consumer

En el método `connect()` del `ChatConsumer`:

```python
async def connect(self):
    # ... (código existente de unirse al grupo y accept) ...

    # Enviar historial de los últimos 3 mensajes
    messages = await self.get_last_messages()
    for msg in messages:
        await self.send(text_data=json.dumps({
            'message': msg['content'],
            'username': msg['username'],
        }))

    # Después enviar "has joined the chat"
    await self.channel_layer.group_send(...)

@database_sync_to_async
def get_last_messages(self):
    from .models import ChatRoom, ChatMessage
    room = ChatRoom.objects.get(name=self.room_name)
    messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')[:3]
    # Devolver en orden cronológico (oldest first)
    return [
        {'content': msg.content, 'username': msg.user.username}
        for msg in reversed(messages)
    ]
```

### Criterios de evaluación (de la corrección)

- [ ] Cuando te unes a un chatroom, aparece un historial de los últimos 3 mensajes publicados en ese chatroom, de arriba abajo, del más antiguo al más reciente

---

## Exercise 03: User List with WebSockets

**Objetivo**: Añadir una lista de usuarios conectados al chatroom que se actualiza automáticamente.

### Implementación

1. **Lista de usuarios conectados**: Cuando un usuario se une, aparece en la lista. Cuando se va, desaparece.

2. **La lista debe estar claramente separada** de los mensajes (otro `<div>` u otro contenedor HTML).

3. **Cuando un usuario se va**: el mensaje `"<username> has left the chat"` aparece después de los mensajes publicados.

4. **La página NO se refresca** (actualización automática vía WebSocket).

### Modificar el Consumer

Necesitamos trackear qué usuarios están conectados. Opciones:

**Opción A: Set en memoria en el consumer (simple)**

```python
class ChatConsumer(AsyncWebsocketConsumer):
    # Variable de clase para trackear usuarios por sala
    room_users = {}  # {'room_name': set('user1', 'user2')}

    async def connect(self):
        # ... código existente ...
        # Añadir usuario a la lista
        if self.room_name not in self.room_users:
            self.room_users[self.room_name] = set()
        self.room_users[self.room_name].add(self.user.username)

        # Enviar lista actualizada a todos
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'users': list(self.room_users[self.room_name]),
            }
        )

    async def disconnect(self, close_code):
        # Quitar usuario de la lista
        if self.room_name in self.room_users:
            self.room_users[self.room_name].discard(self.user.username)

        # Enviar mensaje "<username> has left the chat"
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user.username} has left the chat',
                'username': 'system',
            }
        )

        # Enviar lista actualizada a todos
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'users': list(self.room_users.get(self.room_name, [])),
            }
        )

        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def user_list(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users'],
        }))
```

### Modificar el Template del chatroom

```html
<div id="chat-container" style="display: flex;">
    <div id="messages-container">
        <!-- Mensajes del chat -->
    </div>
    <div id="users-container">
        <h3>Connected Users</h3>
        <ul id="user-list">
            <!-- Se llena dinámicamente vía WebSocket -->
        </ul>
    </div>
</div>
```

### Modificar el JavaScript

```javascript
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.type === 'user_list') {
        // Actualizar la lista de usuarios
        $('#user-list').empty();
        data.users.forEach(function(user) {
            $('#user-list').append('<li>' + user + '</li>');
        });
    } else {
        // Es un mensaje de chat normal
        // Añadir al contenedor de mensajes
    }
};
```

### Criterios de evaluación (de la corrección)

- [ ] La página del chatroom no se refresca sola
- [ ] La lista de usuarios conectados aparece (incluyendo el propio usuario)
- [ ] Entrar y salir de un chatroom con dos usuarios diferentes:
  - [ ] La lista se actualiza automáticamente (aparece el nombre al unirse)
  - [ ] El otro usuario ve la lista actualizada sin refresh
- [ ] Cuando un usuario sale del chatroom, `"<username> has left the chat"` aparece después de los mensajes publicados. Por supuesto, `<username>` es el nombre del usuario que se acaba de ir
- [ ] La lista de usuarios se actualiza automáticamente al salir (desaparece el nombre)

---

## Exercise 04: Pretty Chat (Scroll)

**Objetivo**: Hacer el chat presentable con un contenedor de tamaño fijo y scrollbar automático.

### Implementación

1. **La lista de mensajes** debe estar en un **contenedor de tamaño fijo** (`overflow-y: auto` o `overflow-y: scroll`).

2. **Si los mensajes exceden el contenedor**: desaparecen por arriba y una **scrollbar** aparece al lado.

3. **La scrollbar siempre debe estar posicionada abajo** para que los mensajes más recientes se muestren primero.

### CSS

```css
#messages-container {
    height: 400px;           /* Tamaño fijo */
    overflow-y: auto;        /* Scrollbar cuando se necesite */
    border: 1px solid #ccc;
    padding: 10px;
}
```

### JavaScript (auto-scroll al fondo)

```javascript
function scrollToBottom() {
    const container = document.getElementById('messages-container');
    container.scrollTop = container.scrollHeight;
}

// Llamar después de añadir cada mensaje:
chatSocket.onmessage = function(e) {
    // ... añadir mensaje al DOM ...
    scrollToBottom();
};
```

### Criterios de evaluación (de la corrección)

- [ ] La lista de mensajes aparece en un contenedor de tamaño fijo ("container")
- [ ] Los mensajes que exceden el container desaparecen pero siguen accesibles vía scrollbar
- [ ] La scrollbar siempre está posicionada abajo para que los mensajes más recientes se muestren primero

---

## Checklist global (orden de evaluación)

La evaluación sigue el orden de los ejercicios. Cada ejercicio añade funcionalidad.

### Ex00 — Login with AJAX
- [ ] Crear admin con `./manage.py createsuperuser`
- [ ] La página NO se refresca durante toda la evaluación
- [ ] Sin estar conectado: `127.0.0.1:8000/account/` muestra formulario estándar de login
- [ ] Formulario incorrecto → errores aparecen en la página
- [ ] Formulario correcto → desaparece, botón "Logout" + "Logged as <username>" aparece
- [ ] Cerrar y reabrir la página → sigues logueado, formulario NO aparece
- [ ] Verificar que funciona como admin en `/admin/` (no hay que volver a loguearse)
- [ ] Click en "Logout" → el formulario reaparece. Ir a admin page → hay que loguearse

### Ex01 — Basic Chat with WebSockets
- [ ] 3 links a 3 chatrooms diferentes
- [ ] Acceso imposible sin login
- [ ] Página no se refresca sola
- [ ] Nombre del chatroom visible
- [ ] Mensajes aparecen en orden ascendente, con nombre del usuario
- [ ] Mensajes no desaparecen ni se reemplazan
- [ ] Multi-usuario: "has joined the chat" visible para todos
- [ ] Mensajes de un usuario visibles para todos en la misma sala
- [ ] Usuarios en salas diferentes NO ven los mensajes del otro

### Ex02 — Message History
- [ ] Al unirse, aparecen los últimos 3 mensajes (más antiguo arriba → más nuevo abajo)

### Ex03 — User List
- [ ] Página no se refresca sola
- [ ] Lista de usuarios conectados visible (incluyendo el propio usuario)
- [ ] La lista se actualiza automáticamente al entrar/salir usuarios
- [ ] `"<username> has left the chat"` aparece cuando alguien sale
- [ ] La lista de usuarios se actualiza al salir (nombre desaparece)

### Ex04 — Pretty Chat (Scroll)
- [ ] Mensajes en contenedor de tamaño fijo
- [ ] Mensajes que exceden → desaparecen por arriba + scrollbar
- [ ] Scrollbar siempre posicionada abajo (últimos mensajes visibles)

---

## Notas técnicas importantes

### JQuery — Única librería JS permitida

```html
<!-- CDN de JQuery -->
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
```

No usar ninguna otra librería JavaScript. Todo lo demás se hace con JS vanilla + JQuery.

### CSRF en peticiones AJAX POST

Django requiere el token CSRF en todas las peticiones POST. Para AJAX:

```javascript
// Obtener CSRF token de la cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Configurar JQuery para enviar CSRF en todas las peticiones AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
```

### WebSockets vs AJAX

- **Ex00 (Login/Logout)**: Usar AJAX (`$.ajax()`, `$.post()`). NO WebSockets.
- **Ex01-04 (Chat)**: Usar WebSockets (`new WebSocket()`). NO AJAX.

### AuthenticationForm (pista del subject)

El subject dice "AuthenticationForm, for free!" → usar `django.contrib.auth.forms.AuthenticationForm` para validar login:

```python
from django.contrib.auth.forms import AuthenticationForm

def login_ajax(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return JsonResponse({'success': True, 'username': user.username})
    else:
        errors = {field: errors for field, errors in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors})
```

### InMemoryChannelLayer — Limitación importante

`InMemoryChannelLayer` **solo funciona dentro del mismo proceso**. Si se abren dos pestañas del navegador, ambas se conectan al mismo proceso `runserver`, así que funciona para desarrollo y evaluación. Si se necesita multi-proceso, usar Redis.

### Proteger el chat — Solo usuarios logueados

En el **consumer**, verificar `self.scope['user'].is_authenticated` en `connect()`. Si no está autenticado, cerrar la conexión.

En las **vistas** de chat, usar `LoginRequiredMixin` o decorador equivalente para redirigir a la página de login.

### Bootstrap (opcional pero recomendado para ex04)

```html
<!-- CDN de Bootstrap -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
```

---

## Orden de implementación recomendado

1. **Configuración inicial**: Crear proyecto `d09`, apps `account` y `chat`, instalar `channels`, configurar settings, asgi, urls. `makemigrations` + `migrate`. Crear superusuario.
2. **Ex00**: Vista de account, template con formulario, vistas AJAX login/logout, JavaScript con JQuery. Probar login/logout sin refresh.
3. **Ex01**: Modelos ChatRoom y ChatMessage. Migraciones. Crear 3 chatrooms en BD. Vistas para lista de salas y sala individual. Consumer WebSocket. Routing. Template con JQuery + WebSocket. Probar con 2 usuarios en misma sala y en salas diferentes.
4. **Ex02**: Añadir historial (últimos 3 mensajes) en `connect()` del consumer. Probar entrando a una sala con mensajes previos.
5. **Ex03**: Añadir tracking de usuarios conectados en el consumer. Enviar lista de usuarios actualizada. Mensaje "has left the chat" en `disconnect()`. Actualizar template con contenedor separado para user list. Actualizar JavaScript.
6. **Ex04**: CSS para contenedor de mensajes con tamaño fijo + overflow + auto-scroll al fondo.