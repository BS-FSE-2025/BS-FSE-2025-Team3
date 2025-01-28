from django.test import TestCase, Client
from django.urls import reverse
from Base.models import CustomUser, StudentProfile, LibraryManagerProfile
from Base.forms import SignUpForm, AuthenticationForm, ProfileEditForm
from django.contrib.auth.models import User
from unittest.mock import patch


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
    
    def test_admin_login_view_post_admin_invalid_password(self):
        data = {'username': 'admin', 'password': 'admin13'}
        response = self.client.post(reverse('admin_login'), data)
        self.assertEqual(response.status_code, 200)
       

    def test_admin_login_view_post_admin_valid(self):
        data = {'username': 'admin', 'password': 'admin123'}
        response = self.client.post(reverse('admin_login'), data)
        self.assertEqual(response.status_code, 302)
        #self.assertRedirects(response, reverse('admin_dashboard'))
    
    def test_student_dashboard_view(self):
        self.client.login(username='student', password='student123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard.html')
    
    def test_library_manager_dashboard_view_invalid_password(self):
        self.client.login(username='library_manager', password='librarymanager13')
        response = self.client.get(reverse('library_manager_dashboard'))
        self.assertEqual(response.status_code, 302)
    
    def test_library_manager_dashboard_view_valid(self):
        self.client.login(username='library_manager', password='librarymanager123')
        response = self.client.get(reverse('library_manager_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library_manager_dashboard.html')
    
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
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.get(username='student').check_password('newpassword123'))
        self.assertRedirects(response, reverse('edit_profile'))

