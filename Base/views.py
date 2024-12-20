from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
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

def room_list(request):
    rooms = Room.objects.all()  # בחר את כל החדרים מהדאטהבייס
    return render(request, 'rooms/room_list.html', {'rooms': rooms})

