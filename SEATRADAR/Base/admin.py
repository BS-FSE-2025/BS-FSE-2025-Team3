from django.contrib import admin

# Register your models here.
from .models import Student

admin.site.register (Student)

from .models import librarymanager

admin.site.register(librarymanager)


from .models import Rooms

admin.site.register(Rooms)

from .models import Item
admin.site.register(Item)

from .models import (Library)
admin.site.register(Library)