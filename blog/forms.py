from django import forms
from .models import Photo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['titels', 'description', 'image']