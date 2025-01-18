from django.urls import path
from . import views

urlpatterns = [
    path('', views.say_hello),
    path('process_audio/', views.enhance_audio, name='enhance_audio'),
]
