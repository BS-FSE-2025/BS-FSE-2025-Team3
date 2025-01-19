from django.contrib import admin
from .models import CustomUser, StudentProfile, LibraryManagerProfile, Rooms, Item, Library

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'field_of_study', 'is_active')

@admin.register(LibraryManagerProfile)
class LibraryManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'library_name')

@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display = ('Closed', 'people')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('state', 'num_students', 'last_updated')
