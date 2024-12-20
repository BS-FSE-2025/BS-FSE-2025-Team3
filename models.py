from django.db import models

# Create your models here.
class Student(models.Model):
    username=models.TextField(max_length=200)
    email=models.TextField(max_length=200)
    password=models.TextField(max_length=200)
    

class librarymanager(models.Model):
    username_lm=models.TextField(max_length=200)
    email_lm=models.TextField(max_length=200)
    password_lm=models.TextField(max_length=200)


class Library(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LibraryHours(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="hours")
    date = models.DateField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    class Meta:
        unique_together = ('library', 'date')  # Ensures no duplicate records for the same date and library
        ordering = ['date']  # Orders the records by date

    def __str__(self):
        return f"{self.library.name} - {self.date}"

