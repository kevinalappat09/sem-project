from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject, Chapter, Flashcard
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from datetime import date
from datetime import timedelta

from django.http import HttpResponseBadRequest

from .forms import CustomUserRegistrationForm, CustomUserLoginForm

def home(request):
    subjects = []
    chapters = []
    
    if request.user.is_authenticated:
        subjects = Subject.objects.filter(user=request.user)
        chapters = Chapter.objects.filter(subject__in=subjects)
    
    context = {
        'subjects': subjects,
        'chapters': chapters,
    }

    return render(request, 'flashcards/home.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flashcards:login')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'flashcards/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('flashcards:home')  # Redirect to the home page or any desired page
    else:
        form = CustomUserLoginForm()
    return render(request, 'flashcards/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('flashcards:home')  

def revision(request, chapter_id):
    today = date.today()
    chapter = get_object_or_404(Chapter, id=chapter_id)
    
    # Get the list of flashcards due for revision for this chapter
    flashcards_to_review = Flashcard.objects.filter(
        chapter=chapter,
        next_revision_date=today
    )
    
    # Get the first flashcard due for revision (if any)
    flashcard_to_review = flashcards_to_review.first()
    
    context = {
        'flashcard': flashcard_to_review,
        'chapter_id': chapter.id,
        'flashcards_to_review': flashcards_to_review,
    }
    
    return render(request, 'flashcards/revision.html', context)

@login_required
def next_flashcard(request, flashcard_id, difficulty):
    try:
        flashcard = Flashcard.objects.get(id=flashcard_id)
        
        # Calculate the new next revision date based on the difficulty
        days_between_revisions = (flashcard.next_revision_date - flashcard.previous_revision_date).days
        new_next_revision_date = flashcard.next_revision_date + timedelta(days=(days_between_revisions * float(difficulty)))

        # Update the flashcard's next revision date and previous revision date
        flashcard.next_revision_date = new_next_revision_date
        flashcard.previous_revision_date = date.today()
        flashcard.save()

        # Redirect back to the revision page for the same chapter
        return redirect('flashcards:revision', chapter_id=flashcard.chapter.id)
    except Flashcard.DoesNotExist:
        return HttpResponseBadRequest("Flashcard does not exist.")  