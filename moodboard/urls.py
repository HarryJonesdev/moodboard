from django.urls import path
from . import views
from .views import PostView, PostDetailView, CreatePostView, UpdatePostView, DeletePostView

urlpatterns = [
    path('', PostView.as_view(), name="moodboard-home" ),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name="post-delete"),
    path('post/new/', CreatePostView.as_view(), name="post-create"),
    path('about/', views.about, name="moodboard-about" ),
    
]
