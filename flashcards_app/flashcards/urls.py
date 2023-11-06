from django.urls import path
from . import views

app_name = 'flashcards'

urlpatterns = [
    path('',views.home, name="home"),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('manage/',views.manage_cards,name="manage"),
    path('revision/<int:chapter_id>/', views.revision, name='revision'),
    path('next_flashcard/<int:flashcard_id>/<str:difficulty>/', views.next_flashcard, name='next_flashcard'),
    path('create_chapter/',views.create_chapter,name='create_chapter'),
    path('create_subject/',views.create_subject,name='create_subject'),
    path('add_flashcard/',views.add_flashcard,name='add_flashcard'),
    path('edit_flashcard/<int:flashcard_id>/',views.edit_flashcard,name="edit_flashcard"),
    path('delete_flashcard/<int:flashcard_id>/',views.delete_flashcard,name="delete_flashcard"),
    path('support/',views.support,name='support'),
]