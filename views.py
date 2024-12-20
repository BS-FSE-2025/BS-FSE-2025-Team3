from django.shortcuts import render ,get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from .models import Library, LibraryHours

def home(request):
   return render(request,'home.html')


def singin(request):
   return render(request,'singin.html')

def forgotpassword(request):
   return render(request,'forgotpassword.html')


def updatelibraryh(request):
   return render(request,'updatelibraryh.html')

def update_library_hours(request):
    if request.method == "POST":
        # Handle form submission
        date = request.POST.get("date")
        opening_time = request.POST.get("opening_hours")
        closing_time = request.POST.get("closing_hours")
        library_id = request.POST.get("library_id")  # Optional: If you allow multiple libraries

        try:
            # Ensure date and times are valid
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            opening_time_obj = datetime.strptime(opening_time, "%H:%M").time()
            closing_time_obj = datetime.strptime(closing_time, "%H:%M").time()

            # Assume a single library for simplicity or fetch based on library_id
            library = get_object_or_404(Library, id=library_id) if library_id else Library.objects.first()

            # Create or update the library hours for the specific date
            library_hours, created = LibraryHours.objects.update_or_create(
                library=library,
                date=date_obj,
                defaults={"opening_time": opening_time_obj, "closing_time": closing_time_obj}
            )

            return JsonResponse({"success": True, "message": "Library hours updated successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    # GET request: Render the HTML page
    return render(request, "updatelibraryh.html")
