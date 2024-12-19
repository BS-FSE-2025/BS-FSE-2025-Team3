from django.db import models


class Student(models.Model):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class LibraryManager(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    library_branch = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SystemAdministrator(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    

    
