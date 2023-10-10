from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Chapter, Subject, Flashcard

from datetime import timedelta
from django.utils import timezone



class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'gender', 'college']

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser

class ChapterForm(forms.ModelForm) :
    class Meta : 
        model = Chapter
        fields = ['chapter_name','subject']

class SubjectForm(forms.ModelForm) :
    class Meta:
        model = Subject
        fields = ['subject_name', 'subject_code', 'subject_credits', 'faculty_name']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
    
class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['flashcard_front', 'flashcard_back', 'chapter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the initial values for previous_revision_date, next_revision_date, and difficulty_level
        from datetime import date, timedelta
        
        # Set previous_revision_date to yesterday
        self.initial['previous_revision_date'] = date.today() - timedelta(days=1)
        
        # Set next_revision_date to today
        self.initial['next_revision_date'] = date.today()
        
        # Set difficulty_level to "Easy"
        self.initial['difficulty_level'] = 'Easy'

class FlashcardEditForm(forms.ModelForm) :
    class Meta :
        model = Flashcard
        fields = ['flashcard_front','flashcard_back']