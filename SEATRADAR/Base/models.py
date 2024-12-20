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

    
class Rooms (models.Model):
    # name_room=models.CharField(max_length=200)
    Closed=models.TextField(max_length=30)
    people=models.IntegerField()
    
def __str__(self):
    return self.name_room
    

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Library(models.Model):
    state=models.CharField(max_length=20,null=True)
    num_students=models.PositiveIntegerField(null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    
    