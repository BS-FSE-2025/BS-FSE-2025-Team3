from django.db import models


# Create your models here.
class Student(models.Model):
    username=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    password=models.CharField(max_length=200)
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')

    def __str__(self):
        return f"Student: {self.name}, Email: {self.email},ID:{self.id}"  
    
    
class librarymanager(models.Model):
    username_lm=models.TextField(max_length=200)
    email_lm=models.EmailField(max_length=200)
    password_lm=models.TextField(max_length=200)
    def __str__(self):
        return f"Manger: {self.username_lm}, Email: {self.email_lm}"  



class Room(models.Model):
    
    name = models.CharField(max_length=100, unique=True) 
    size = models.FloatField()  # גודל החדר במ"ר
    max_occupants = models.IntegerField()  # מספר האנשים המקסימלי
    is_available = models.BooleanField(default=True)  # האם החדר זמין 

    def __str__(self):
        return f"Room {self.name} Capacity ({self.max_occupants} Size {self.size} availabilty{self.is_available})"
class Library(models.Model):
    
    name = models.CharField(max_length=100, unique=True) 
    size = models.FloatField()  # גודל המקום במ"ר
    max_occupants = models.IntegerField()  # מספר האנשים המקסימלי
    is_available = models.BooleanField(default=True)  # האם המקום זמין 

    def __str__(self):
        return f"Library {self.name} Capacity ({self.max_occupants} Size {self.size} availabilty{self.is_available})"