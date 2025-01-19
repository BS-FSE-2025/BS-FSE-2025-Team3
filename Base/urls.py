from django.urls import path
from . import views




urlpatterns = [
 path('',views.home,name="home"),
 path('singin.html/',views.singin,name="singin"),
 path('signup/', views.signup, name='signup'),
 path('forgotpassword.html/',views.forgotpassword,name="forgotpassword"),
 path('Item.html/', views.item_list, name='Item'),
#  path('library.html/',views.library_items,name='library_items'),
 path('library.html/', views.last_updated_library, name='last_updated_library'),
 path('update_library_state/', views.update_library_state, name='update_library_state'),
path('home/', views.home, name='home'),
path('student_dashboard.html/', views.student_dashboard, name='student_dashboard'),
path('library_manager_dashboard.html/', views.library_manager_dashboard, name='library_manager_dashboard'),
path('edit_profile.html/', views.edit_profile, name='edit_profile'),



]
