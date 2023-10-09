from django.urls import path
from . import views

app_name = 'flashcards'

urlpatterns = [
    path('home/',views.home, name="home"),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('revision/<int:chapter_id>/', views.revision, name='revision'),
    path('next_flashcard/<int:flashcard_id>/<str:difficulty>/', views.next_flashcard, name='next_flashcard'),
]