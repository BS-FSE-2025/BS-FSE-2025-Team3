from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from Base import views
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode




urlpatterns = [
 path('',views.home,name="home"),
 path('singin.html/',views.singin,name="singin"),
 path('signup/', views.signup, name='signup'),
 path('admin_login/', views.admin_login, name='admin_login'),
 path('forgotpassword.html/',views.forgotpassword,name="forgotpassword"),
  path('Availablerooms.html/',views.Availablerooms,name="Availablerooms"),

 path('Item.html/', views.item_list, name='Item'),
#  path('library.html/',views.library_items,name='library_items'),
 path('library.html/', views.last_updated_library, name='last_updated_library'),
 path('update_library_state/', views.update_library_state, name='update_library_state'),
path('home/', views.home, name='home'),
path('admin_dashboard,html/', views.admin_dashboard, name='admin_dashboard'),
path('student_dashboard.html/', views.student_dashboard, name='student_dashboard'),
path('library_manager_dashboard.html/', views.library_manager_dashboard, name='library_manager_dashboard'),
path('edit_profile.html/', views.edit_profile, name='edit_profile'),

path('singin.html/forgotpassword.html/invaled_email.html/', views.invaled_email, name='invaled_email'),
path('singin.html/forgotpassword.html/invaled_token.html/', views.invaled_token, name='invaled_token'),
path('singin.html/forgotpassword.html/', views.request_password_reset, name='forgotpassword'),
path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
path('password_rest_email.html/',views.password_reset_email,name="password_rest_email"),
path('password_reset_complete.html/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
path('singin.html/forgotpassword.html/email_sended.html/',views.email_sended,name='email_sended'),



]
