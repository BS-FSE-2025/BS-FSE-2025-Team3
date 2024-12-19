from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Student, SystemAdministrator, LibraryManager
from django.contrib.auth import authenticate, login


# Helper Function: Save User with Validation
def save_user(model, username, email, password):
    """
    Saves a user to the database with hashed password after validation.
    """
    user = model(username=username, email=email)
    user.set_password(password)  # Hash the password
    user.save()
    return user


# Helper Function: Validate Form Inputs
def validate_signup_form(username, email, password, model):
    """
    Validates the username, email, and password for signup.
    Returns error message if validation fails, otherwise None.
    """
    try:
        validate_email(email)
    except ValidationError:
        return 'Invalid email address.'

    if model.objects.filter(username=username).exists():
        return 'Username is already taken.'
    if model.objects.filter(email=email).exists():
        return 'Email is already registered.'
    if len(password) < 8:
        return 'Password must be at least 8 characters long.'
    return None


# Home Page View
def homepage(request):
    return render(request, 'OurWeb/homepage.html')


# Sign-Up Role Selection View
def signup_selection(request):
    return render(request, 'OurWeb/signup.html')


# Generalized Sign-Up View
def signup(request, model, template_name, redirect_view):
    """
    A generalized view for signup logic shared across all roles.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate inputs
        error = validate_signup_form(username, email, password, model)
        if error:
            messages.error(request, error)
        else:
            try:
                save_user(model, username, email, password)
                messages.success(request, 'You have signed up successfully!')
                return redirect(redirect_view)
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return render(request, template_name)


# Student Sign-Up View
def student_signup(request):
    return signup(request, Student, 'OurWeb/student_signup.html', 'student_login')


# Library Manager Sign-Up View
def manager_signup(request):
    return signup(request, LibraryManager, 'OurWeb/manager_signup.html', 'student_login')


# Admin Sign-Up View
def admin_signup(request):
    return signup(request, SystemAdministrator, 'OurWeb/admin_signup.html', 'student_login')


# Student Login View
def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('homepage')  # Redirect to homepage
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'OurWeb/homepage.html')

# Role-Based Login View
def login_with_role(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Redirect based on user role
            if hasattr(user, 'student'):
                return redirect('student_dashboard')
            elif hasattr(user, 'librarymanager'):
                return redirect('manager_dashboard')
            elif hasattr(user, 'systemadministrator'):
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Role not recognized.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'OurWeb/login.html')