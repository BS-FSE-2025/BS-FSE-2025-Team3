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
    
    name = models.CharField(max_length=100, unique=True) 
    size = models.FloatField()  
    max_occupants = models.IntegerField()  
    is_available = models.BooleanField(default=True)

    def _str_(self):
        return f"Library {self.name} Capacity ({self.max_occupants} Size {self.size} availabilty{self.is_available})"