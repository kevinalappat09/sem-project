from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject, Chapter, Flashcard
from django.db.models import Count,Q
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from datetime import date, timedelta

from django.http import HttpResponseBadRequest

from .forms import CustomUserRegistrationForm, CustomUserLoginForm, ChapterForm,SubjectForm, FlashcardForm, FlashcardEditForm


# Home page code
def home(request):
    subjects = []
    chapters = []
    
    if request.user.is_authenticated:
        subjects = Subject.objects.filter(user=request.user)
        chapters = Chapter.objects.filter(subject__in=subjects)

        for chapter in chapters:
            today = date.today()
            flashcards_due_today = Flashcard.objects.filter(
                chapter=chapter,
                next_revision_date=today,
            )
            chapter.revision_count = flashcards_due_today.count()

    context = {
        'subjects': subjects,
        'chapters': chapters,
    }

    return render(request, 'flashcards/home.html', context)

# Code the registration page
def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flashcards:login')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'flashcards/register.html', {'form': form})

# Code for the login page
def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('flashcards:home') 
    else:
        form = CustomUserLoginForm()
    return render(request, 'flashcards/login.html', {'form': form})

# Logout page
@login_required
def user_logout(request):
    logout(request)
    return redirect('flashcards:home')  

# Revision page.
def revision(request, chapter_id):
    today = date.today()
    chapter = get_object_or_404(Chapter, id=chapter_id)
    flashcards_to_review = Flashcard.objects.filter(
        chapter=chapter,
        next_revision_date=today
    )
    flashcard_to_review = flashcards_to_review.first()
    context = {
        'flashcard': flashcard_to_review,
        'chapter_id': chapter.id,
        'flashcards_to_review': flashcards_to_review,
    }
    
    return render(request, 'flashcards/revision.html', context)

# Sets the new revision schedule for a flashcard.
@login_required
def next_flashcard(request, flashcard_id, difficulty):
    try:
        flashcard = Flashcard.objects.get(id=flashcard_id)
        
        days_between_revisions = (flashcard.next_revision_date - flashcard.previous_revision_date).days
        new_next_revision_date = flashcard.next_revision_date + timedelta(days=(days_between_revisions * float(difficulty)))

        flashcard.next_revision_date = new_next_revision_date
        flashcard.previous_revision_date = date.today()
        flashcard.save()

        # Redirect back to the revision page for the same chapter
        return redirect('flashcards:revision', chapter_id=flashcard.chapter.id)
    except Flashcard.DoesNotExist:
        return HttpResponseBadRequest("Flashcard does not exist.")  

# Manages all the cards.
def manage_cards(request) :
    chapters = Chapter.objects.filter(subject__user=request.user)
    selected_chapter_id = request.GET.get('chapter_id')

    flashcards = []
    if selected_chapter_id:
        flashcards = Flashcard.objects.filter(chapter__id=selected_chapter_id)

    return render(request, 'flashcards/manage.html', {
        'chapters': chapters,
        'flashcards': flashcards,
        'selected_chapter_id': int(selected_chapter_id) if selected_chapter_id else None,
    })

def create_chapter(request) :
    if request.method == 'POST':
        form = ChapterForm(request.user, request.POST)
        if form.is_valid():
            # Process the form data
            chapter = form.save()
            return redirect('flashcards:manage')
    else:
        form = ChapterForm(request.user)
    return render(request, 'flashcards/create_chapter.html', {'form': form}) 

def create_subject(request) :
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            # Create an instance of the subject, but don't save it yet
            subject = form.save(commit=False)
            # Assign the selected color to the subject
            subject.color = form.cleaned_data['color']
            # Assign the user
            subject.user = request.user
            subject.save()  # Now save the subject
            return redirect('flashcards:manage')
    else:
        form = SubjectForm()
    return render(request, 'flashcards/create_subject.html', {'form': form})

def add_flashcard(request):
    if request.method == 'POST':
        form = FlashcardForm(request.user, request.POST)
        if form.is_valid():
            flashcard = form.save()
            return redirect('flashcards:manage')
    else:
        form = FlashcardForm(request.user)
    return render(request, 'flashcards/add_flashcard.html', {'form': form})

def edit_flashcard(request,flashcard_id) :
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    if request.method == 'POST':
        form = FlashcardEditForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect('flashcards:manage')  
    else:
        form = FlashcardEditForm(instance=flashcard)
    return render(request, 'flashcards/edit_flashcard.html', {'flashcard': flashcard, 'form': form})
        

def delete_flashcard(request, flashcard_id) :
    flashcard = get_object_or_404(Flashcard,id=flashcard_id)
    if request.method == 'POST' :
        flashcard.delete()
        return redirect('flashcards:manage')
    
    return render(request,'flashcards/confirm_deletion.html',{'flashcard':flashcard})