from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import date, timedelta

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    college = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20, unique=True)
    subject_credits = models.PositiveIntegerField()
    faculty_name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name



class Chapter(models.Model):
    chapter_name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.chapter_name


class Flashcard(models.Model):
    flashcard_front = models.TextField()
    flashcard_back = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    previous_revision_date = models.DateField(default=date.today() - timedelta(days=1))
    next_revision_date = models.DateField(default=date.today())
    DIFFICULTY_CHOICES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Easy')

    def __str__(self):
        return self.flashcard_front
