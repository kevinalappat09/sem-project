from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject, Chapter, Flashcard
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from datetime import date
from datetime import timedelta

from django.http import HttpResponseBadRequest

from .forms import CustomUserRegistrationForm, CustomUserLoginForm, ChapterForm,SubjectForm, FlashcardForm, FlashcardEditForm


# Home page code
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
            return redirect('flashcards:home')  # Redirect to the home page or any desired page
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

# Manages all the cards.
def manage_cards(request) :
    chapters = Chapter.objects.all()
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
    if request.method == 'POST' :
        form = ChapterForm(request.POST)
        if form.is_valid() :
            form.save()
            return redirect('flashcards:manage')
    else :
        form = ChapterForm()
    return render(request, 'flashcards/create_chapter.html', {'form' : form})   

def create_subject(request) :
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            # Set the user before saving
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect('flashcards:manage')
    else:
        form = SubjectForm()
    
    return render(request, 'flashcards/create_subject.html', {'form': form})

def add_flashcard(request) :
    if request.method == 'POST' :
        form = FlashcardForm(request.POST)
        if form.is_valid() :
            flashcard = form.save()
            return redirect('flashcards:manage')
    else :
        form = FlashcardForm()
    return render(request,'flashcards/add_flashcard.html',{'form':form})

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