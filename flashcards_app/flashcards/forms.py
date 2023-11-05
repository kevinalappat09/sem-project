from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Chapter, Subject, Flashcard

from datetime import timedelta
from django.utils import timezone



class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'gender', 'college']

    def __init__(self, *args, **kwargs) :
        super(CustomUserRegistrationForm,self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class':'form-input'})
        self.fields['email'].widget.attrs.update({'class':'form-input'})
        self.fields['password1'].widget.attrs.update({'class':'form-input'})
        self.fields['password2'].widget.attrs.update({'class':'form-input'})
        self.fields['first_name'].widget.attrs.update({'class':'form-input'})
        self.fields['last_name'].widget.attrs.update({'class':'form-input'})
        self.fields['phone_number'].widget.attrs.update({'class':'form-input'})
        self.fields['gender'].widget.attrs.update({'class':'form-input'})
        self.fields['college'].widget.attrs.update({'class':'form-input'})

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username','password']
    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-input'})
        self.fields['password'].widget.attrs.update({'class':'form-input'})


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['chapter_name', 'subject']

    def __init__(self, user, *args, **kwargs):
        super(ChapterForm, self).__init__(*args, **kwargs)
        self.fields['chapter_name'].widget.attrs.update({'class': 'form-input'})
        self.fields['subject'].widget.attrs.update({'class': 'form-dropdown'})

        # Filter the subjects based on the user
        if user.is_authenticated:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)

class SubjectForm(forms.ModelForm):
    COLOR_CHOICES = (
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('pink', 'Pink'),
    )

    subject_color = forms.ChoiceField(
        label='Subject Color',
        choices=COLOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Subject
        fields = ['subject_name', 'subject_code', 'subject_credits', 'faculty_name']

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['subject_name'].widget.attrs.update({'class': 'form-input'})
        self.fields['subject_code'].widget.attrs.update({'class': 'form-input'})
        self.fields['subject_credits'].widget.attrs.update({'class': 'form-input'})
        self.fields['faculty_name'].widget.attrs.update({'class': 'form-input'})

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

    def __init__(self, user, *args, **kwargs):
        super(FlashcardForm, self).__init__(*args, **kwargs)
        self.fields['flashcard_front'].widget.attrs.update({'class': 'form-input'})
        self.fields['flashcard_back'].widget.attrs.update({'class': 'form-input'})
        self.fields['chapter'].widget.attrs.update({'class': 'form-dropdown'})

        # Filter the chapter queryset to show only the user's chapters
        self.fields['chapter'].queryset = Chapter.objects.filter(subject__user=user)
        
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