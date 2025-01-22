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
        fields = ['first_name', 'last_name', 'email', 'username', 'profile_photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
        }

    def clean_profile_photo(self):
        photo = self.files.get('profile_photo')  # Access the file from the request.FILES dictionary
        if photo:
            # Check file size
            if photo.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("The uploaded file is too large (max 5MB).")

            # Check file type
            if not photo.content_type.startswith('image/'):
                raise forms.ValidationError("Invalid file type. Please upload an image.")
        return photo