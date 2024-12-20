from django.urls import path
from . import views


urlpatterns =[
path('',views.home,name="home"),
path('singin.html/',views.singin,name="singin"),
path('forgotpassword.html/',views.forgotpassword,name="forgotpassword"),
path('Availablerooms.html/',views.Availablerooms,name="Availablerooms"),
path('AvailableLibrary.html/',views.AvailableLibrary,name="AvailableLibrary"),
path('updatelibraryh.html/',views.updatelibraryh,name="updatelibraryh")
]