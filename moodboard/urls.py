from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="moodboard-home" ),
    path('about/', views.about, name="moodboard-about" ),
    
]
