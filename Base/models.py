from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save 
import logging
 
logger = logging.getLogger(__name__)


# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('library_manager', 'Library Manager'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, null=False)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    def get_dashboard_url(self):
        if self.user_type == 'student':
            return '/student_dashboard/'
        elif self.user_type == 'library_manager':
            return '/library_manager_dashboard/'
        elif self.user_type == 'admin':
            return '/admin_dashboard/'
        return '/'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


# Student Profile Model
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    field_of_study = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Student: {self.user.username} ({self.field_of_study})"


# Library Manager Profile Model
class LibraryManagerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='library_manager_profile')
    library_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Library Manager: {self.user.username}"
    
    # Admin Profile Model
class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    department = models.CharField(max_length=255, blank=True, null=True)  # Optional department field
    contact_number = models.CharField(max_length=15, blank=True, null=True)  # Optional contact number

    def __str__(self):
        return f"Admin: {self.user.username} (Department: {self.department or 'N/A'})"


# Consolidated Signal for Profile Management
@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Automatically create or update the appropriate profile based on the user_type.
    """
    if created:
        logger.info(f"Creating profile for user: {instance.username}, user_type: {instance.user_type}")
        if instance.user_type == 'student':
            StudentProfile.objects.get_or_create(user=instance)
        elif instance.user_type == 'library_manager':
            LibraryManagerProfile.objects.get_or_create(user=instance)
        elif instance.user_type == 'admin':
           AdminProfile.objects.get_or_create(user=instance)

# Rooms Model
class Rooms(models.Model):
    Closed = models.TextField(max_length=30)  # "Closed" status description
    people = models.IntegerField()  # Number of people currently in the room

    def __str__(self):
        return f"Room Status: {self.Closed}, People: {self.people}"

# Item Model
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Library Model
class Library(models.Model):
    state = models.CharField(max_length=20, null=True)
    num_students = models.PositiveIntegerField(null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Library State: {self.state or 'Unknown'}, Students: {self.num_students or 0}, Last Updated: {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')}"



class Sensor(models.Model):
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    last_checked = models.DateTimeField(auto_now=True)