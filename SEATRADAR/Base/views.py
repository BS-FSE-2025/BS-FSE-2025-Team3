from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.http import HttpResponse
from .models import Rooms
from .models import Item
from .models import Library


def library_items(request):
   library=Library.objects.all()
   return render(request,'library.html',{'library':library})




def item_list(request):
    items = Item.objects.all()  
    return render(request, 'Item.html', {'items': items})


def home(request):
  
   return render(request,'home.html')
   
   


def singin(request):
   return render(request,'singin.html')

def forgotpassword(request):
   return render(request,'forgotpassword.html')



def last_updated_library(request):
    last_library = Library.objects.order_by('-last_updated').first() 
    return render(request, 'library.html', {'last_library': last_library})

def update_library_state(request):
    if request.method == 'POST':
        state = request.POST.get('library_state')
        last_library = Library.objects.order_by('-last_updated').first()
        if last_library:
            last_library.state = state
            last_library.last_updated = now()
            last_library.save()
        return redirect('last_updated_library')
    return HttpResponse("Invalid request", status=400)

