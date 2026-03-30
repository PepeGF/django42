from . import views
from django.urls import path

# when included at project level under 'ex00/', use an empty path here
urlpatterns = [
    # esta url es para localhost:8000/ex00/
    path('', views.index, name='ex00'),
]