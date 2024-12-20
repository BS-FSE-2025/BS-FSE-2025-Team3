from django.urls import path
from . import views


urlpatterns =[
path('',views.home,name="home"),
path('singin.html/',views.singin,name="singin"),
path('forgotpassword.html/',views.forgotpassword,name="forgotpassword"),
 path('Item.html/', views.item_list, name='Item'),
#  path('library.html/',views.library_items,name='library_items'),
 path('library.html/', views.last_updated_library, name='last_updated_library'),
 path('update_library_state/', views.update_library_state, name='update_library_state'),
]
