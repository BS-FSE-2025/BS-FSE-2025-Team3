from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Rooms, Item, Library, StudentProfile, LibraryManagerProfile
from .forms import SignUpForm, ProfileEditForm
import logging

logger = logging.getLogger(__name__)

User = get_user_model()  # Use Django's custom user model

def home(request):
    return render(request, 'home.html')

def library_items(request):
    library = Library.objects.all()
    return render(request, 'library.html', {'library': library})


def item_list(request):
    items = Item.objects.all()
    return render(request, 'Item.html', {'items': items})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = form.cleaned_data['user_type']  # Set user_type from form data
            user.save()

            # Create the appropriate profile
            if user.user_type == 'student':
                StudentProfile.objects.get_or_create(user=user)
            elif user.user_type == 'library_manager':
                LibraryManagerProfile.objects.get_or_create(user=user)

            # Log the user in
            login(request, user)
            redirect_url = 'student_dashboard' if user.user_type == 'student' else 'library_manager_dashboard'
            return redirect(redirect_url)   
        else:
            messages.error(request, f"Form Errors: {form.errors}")
    else:
        form = SignUpForm()
    return render(request, 'singin.html', {'form': form})

def singin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('student_dashboard' if user.user_type == 'student' else 'library_manager_dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'singin.html', {'form': form})

@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

@login_required
def library_manager_dashboard(request):
    return render(request, 'library_manager_dashboard.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was updated successfully.")
            redirect_url = 'student_dashboard' if request.user.user_type == 'student' else 'library_manager_dashboard'
            return redirect(redirect_url)
        else:
            messages.error(request, "Error updating your profile.")
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

def forgotpassword(request):
    return render(request, 'forgotpassword.html')

def last_updated_library(request):
    last_library = Library.objects.order_by('-last_updated').first()
    return render(request, 'library.html', {'last_library': last_library})

@login_required
def update_library_state(request):
    if request.method == 'POST':
        state = request.POST.get('library_state')
        last_library = Library.objects.order_by('-last_updated').first()
        if last_library:
            last_library.state = state
            last_library.last_updated = now()
            last_library.save()
            return redirect('last_updated_library')
        else:
            messages.error(request, "No library data found to update.")
    return HttpResponse("Invalid request", status=400)
