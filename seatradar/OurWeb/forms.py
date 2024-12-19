from django import forms
from .models import Student, LibraryManager, SystemAdministrator

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'password']
    
class LibraryManagerForm(forms.ModelForm):
    class Meta:
        model = LibraryManager
        fields = ['name', 'email', 'library_branch']

class AdminForm(forms.ModelForm):
    class Meta:
        model = SystemAdministrator
        fields = ['username', 'email', 'password']

