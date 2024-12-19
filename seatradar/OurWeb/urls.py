from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signup/', views.signup_selection, name='signup'),
    path('signup/student/', views.student_signup, name='student'),
    path('signup/manager/', views.manager_signup, name='manager'),
    path('signup/admin/', views.admin_signup, name='admin'),
    path('login/student/', views.student_login, name='student_login'),
    path('login/', views.login_with_role, name='login_with_role'),

]
