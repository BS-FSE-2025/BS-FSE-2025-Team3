from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from Base.models import CustomUser


# Sign-up form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2' , 'user_type')

    def clean_user_type(self):
        user_type = self.cleaned_data.get('user_type')
        if user_type == 'admin':
            raise forms.ValidationError("You cannot sign up as an admin.")
        return user_type
        

# Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email/Username')
    password = forms.CharField(widget=forms.PasswordInput)


    
class ProfileEditForm(forms.ModelForm):
     class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'profile_photo']  # Fields for profile editing
        widgets = {
            'profile_photo': forms.FileInput(attrs={'accept': 'image/*'}),
        }

