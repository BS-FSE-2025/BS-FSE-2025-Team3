from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Rooms, Item, Library, StudentProfile, LibraryManagerProfile
from .forms import SignUpForm, ProfileEditForm
import logging
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from .opencv_stream import generate_frames, get_people_count  # OpenCV scripts


def user_logout(request):
    """Logs out the user and redirects to the login page"""
    logout(request)
    return redirect('singin')  # Redirects to the login page after logout

# Fix: Correct template file and pass Up, Down, and Net counts
def index(request):
    up_count, down_count = get_people_count()
    net_count = up_count - down_count  # Compute Net Count (Up - Down)
    return render(request, 'index.html', {"up": up_count, "down": down_count, "net": net_count})

# Fix: Ensure real-time updates for the Net Count
def get_counter_data(request):
    up_count, down_count = get_people_count()
    net_count = up_count - down_count
    return JsonResponse({'up_count': up_count, 'down_count': down_count, 'net_count': net_count})

# Fix: Ensure the video stream works correctly
def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace; boundary=frame")

logger = logging.getLogger(__name__)

User = get_user_model()  # Use Django's custom user model

def library_items(request):
    library = Library.objects.all()
    return render(request, 'library.html', {'library': library})


def item_list(request):
    items = Item.objects.all()
    return render(request, 'Item.html', {'items': items})

def home(request):
    return render(request, 'home.html')

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


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is an admin
            if user.user_type == 'admin':
                login(request, user)
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            else:
                # If the user is not an admin, show an error message
                messages.error(request, 'Access denied. You are not authorized as an admin.')
        else:
            # Invalid credentials
            messages.error(request, 'Invalid username or password.')

    return render(request, 'admin_login.html')

@login_required
def student_dashboard(request):
    """ Passes counter data to the student dashboard """
    up_count, down_count = get_people_count()
    net_count = up_count - down_count
    return render(request, 'student_dashboard.html', {"up": up_count, "down": down_count, "net": net_count})
@login_required
def library_manager_dashboard(request):
    return render(request, 'library_manager_dashboard.html')

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return redirect('admin_login')  # Restrict access if the user is not an admin
    return render(request, 'admin_dashboard.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Profile form for updating user information
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")

        # Check if the password form is valid
        if password_form.is_valid():
            user = password_form.save()  # Save the new password in the database
            update_session_auth_hash(request, user)  # Keep the user logged in after the password change
            messages.success(request, "Your password has been updated successfully!")
            return redirect('edit_profile')  # Redirect to avoid resubmission
        elif password_form.has_changed():  # Show an error if the user attempted to change the password but failed
            messages.error(request, "Password change failed. Please correct the errors below.")

    else:
        # Initialize forms for GET requests
        profile_form = ProfileEditForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    # Render the forms in the template
    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })


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
    return HttpResponse("Invalid request",status=400)
def map (request):
 return render (request,'map.html')

def test(request):
 return render (request,'test.html')

