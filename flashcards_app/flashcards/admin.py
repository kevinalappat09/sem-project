from django.contrib import admin
from .models import CustomUser, Subject, Chapter, Flashcard

admin.site.register(CustomUser)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Flashcard)
