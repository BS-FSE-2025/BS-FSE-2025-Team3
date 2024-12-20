from django.shortcuts import render
from django.http import HttpResponse
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

