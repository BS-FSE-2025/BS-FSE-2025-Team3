from django.test import TestCase, Client
from django.urls import reverse
from Base.models import CustomUser, StudentProfile, LibraryManagerProfile
from Base.forms import SignUpForm, AuthenticationForm, ProfileEditForm
from .forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.core import mail
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator


class ViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.student_user = CustomUser.objects.create_user(username='student', password='student123', user_type='student')
        self.library_manager_user = CustomUser.objects.create_user(username='library_manager', password='librarymanager123', user_type='library_manager')
        self.admin_user = CustomUser.objects.create_user(username='admin', password='admin123', user_type='admin')
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'singin.html')
    
    def test_signup_view_post_student(self):
      data = {
        'username': 'newstudent',
        'password1': 'StrongPassword!23',
        'password2': 'StrongPassword!23',
        'user_type': 'student',
        'email': 'newstudent@example.com'
     }
      response = self.client.post(reverse('signup'), data)
      if response.status_code == 200 and 'form' in response.context:
        errors = response.context['form'].errors
      else:
        errors = None
      self.assertEqual(response.status_code, 302, msg=f"Form errors: {errors if errors else 'No form errors context available'}")
      self.assertRedirects(response, reverse('student_dashboard'))
      self.assertTrue(CustomUser.objects.filter(username='newstudent').exists())
      self.assertTrue(StudentProfile.objects.filter(user__username='newstudent').exists())


    def test_singin_view_get(self):
        response = self.client.get(reverse('singin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'singin.html')
    
    def test_singin_view_post(self):
        data = {'username': 'student', 'password': 'student123'}
        response = self.client.post(reverse('singin'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('student_dashboard'))
    
    def test_admin_login_view_get(self):
        response = self.client.get(reverse('admin_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_login.html')
    
    def test_admin_login_view_post_admin(self):
        data = {'username': 'admin', 'password': 'admin123'}
        response = self.client.post(reverse('admin_login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin_dashboard'))
    
    def test_student_dashboard_view(self):
        self.client.login(username='student', password='student123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard.html')
    
    def test_library_manager_dashboard_view(self):
        self.client.login(username='library_manager', password='librarymanager123')
        response = self.client.get(reverse('library_manager_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library_manager_dashboard.html')
    
    def test_admin_dashboard_view(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard.html')
    
    def test_edit_profile_view_get(self):
        self.client.login(username='student', password='student123')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
    
    def test_edit_profile_view_post(self):
        self.client.login(username='student', password='student123')
        data = {
            'first_name': 'NewName',
            'old_password': 'student123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        }
        response = self.client.post(reverse('edit_profile'), data)
        self.assertEqual(response.status_code, 302)  # Check for redirect status code
        self.assertTrue(CustomUser.objects.get(username='student').check_password('newpassword123'))
        self.assertRedirects(response, reverse('edit_profile'))  # Check redirection URL



###---בדיקת יחידה לשחזור הסיסמה----###
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator  # ייבוא המחולל טוקנים

class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

    def test_request_password_reset_valid_email(self):
        response = self.client.post(reverse('forgotpassword'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        
    def test_request_password_reset_invalid_email(self):
        response = self.client.post(reverse('forgotpassword'), {'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, 302)

    def test_password_reset_confirm_valid_token(self):
        self.client.logout()  # ודא שהמשתמש לא מחובר
        token = default_token_generator.make_token(self.user)  # יצירת טוקן לשחזור סיסמה
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 302)

    def test_password_reset_confirm_invalid_token(self):
        self.client.logout()  # ודא שהמשתמש לא מחובר
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': 'invalid-token'}))
        self.assertEqual(response.status_code, 200)

