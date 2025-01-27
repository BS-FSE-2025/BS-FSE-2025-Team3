from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Rooms, Item, Library, StudentProfile, LibraryManagerProfile
from .forms import SignUpForm, ProfileEditForm
import logging
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.http import Http404
from django.utils.crypto import get_random_string
import re
import logging
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from .models import CustomUser
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import force_str
import json
from .models import Rooms
logger = logging.getLogger(__name__)

User = get_user_model()  # Use Django's custom user model



def forgotpassword(request):
    return render(request, 'forgotpassword.html')
def home(request):
    return render(request,'home.html')

def singin(request):
    return render(request,'singin.html')

def forgotpassword(request):
    return render(request,'forgotpassword.html')

def Availablerooms(request):
    return render(request,'Availablerooms.html')

def AvailableLibrary(request):
    return render(request,'AvailableLibrary.html')

def updatelibraryh(request):
    return render(request,'updatelibraryh.html')



def password_reset_done(request):
    return render(request,'password_reset_done.html')

def password_reset_email(request):
    return render(request,'password_reset_email.html')
def email_sended(request):
    return render(request,'email_sended.html')

def password_reset_form(request):
    return render(request,'password_reset_form.html')
def password_reset_confirm(request):
    return render(request,'password_reset_confirm.html')
def password_reset_complete(request):
    return render(request,'password_reset_complete.html')
def invaled_email(request):
    return render(request,'invaled_email.html')
def invaled_token(request):
    return render(request,'invaled_token.html')

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
    return render(request, 'student_dashboard.html')

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




###-----REST PASSWORD-----###
def request_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # בודקים אם המשתמש קיים במערכת
        try:
               
            user = get_user_model().objects.get(email=email)
           
            # יצירת טוקן לשחזור סיסמה
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # יצירת קישור לשחזור סיסמה
            reset_url = f"{'http://127.0.0.1:8000'}/password_reset_confirm/{uid}/{token}/"

            # הגדרת נושא ותוכן המייל
            subject = 'בקשה לשחזור סיסמה'
            message = render_to_string('password_rest_email.html', {
                'user': user,
                'reset_url': reset_url,
            })

            # שליחת המייל
            send_mail(subject, message, 'safaa0bnt0aboha@gmail.com', [email])

            # הודעה שהמייל נשלח
            messages.success(request, 'אם כתובת המייל קיימת, שלחנו לך קישור לשחזור סיסמה!')
            return redirect('email_sended.html')  # הכתובת הזו תלויה בשם ה-view שלך

        except get_user_model().DoesNotExist:
            # אם המשתמש לא קיים,ר
            messages.error(request, 'כתובת הדואר האלקטרוני לא נמצאה במערכת.')
            return redirect('invaled_email.html')  
        
    return render(request,'forgotpassword.html')

######################################################################3

# View לשחזור סיסמה (כאשר המשתמש לוחץ על הקישור במייל)
def password_reset_confirm(request, uidb64, token):
    try:
        # מפענח את ה-UID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        # מאמת את הטוקן
        if not default_token_generator.check_token(user,' token'):
            messages.error(request, 'הקישור לשחזור סיסמה לא תקף או פג תוקפו.')
            return redirect('invaled_token.html')
        
        if request.method == 'POST':
            # יצירת טופס איפוס סיסמה
            form =  PasswordResetForm(user=user, data=request.POST)
            if form.is_valid():
                # עדכון הסיסמה במודל
                form.save() 
                return HttpResponse('הסיסמה שלך שוחזרה בהצלחת')
                messages.success(request, 'הסיסמה שלך שוחזרה בהצלחה!')
                 # הכתובת הזו תלויה בשם ה-view שלך

                return redirect('singin.html')  # או דף התחברות או דף אחר
        else:
            form =  PasswordResetForm(user=user)

        return render(request, 'password_reset_confirm.html', {'form': form})
    
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request, 'הקישור לשחזור סיסמה לא תקף או פג תוקפו.')
        return redirect('invaled_token.html')
    

def password_reset_done(request):
    return render(request, 'password_reset_done.html')
