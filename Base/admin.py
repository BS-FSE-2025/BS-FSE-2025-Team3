from django.contrib import admin
from .models import CustomUser, StudentProfile, LibraryManagerProfile, AdminProfile, Rooms, Item, Library, Sensor

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_superuser')
    list_filter = ('user_type',)
    search_fields = ('username', 'email')
    readonly_fields = ('last_login', 'date_joined')  # Example of read-only fields

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'field_of_study', 'is_active')

@admin.register(LibraryManagerProfile)
class LibraryManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'library_name')

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.user:
            raise ValueError("You must associate a valid user with the AdminProfile.")
        super().save_model(request, obj, form, change)

@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display = ('Closed', 'people')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('state', 'num_students', 'last_updated')

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('location', 'status','last_checked')