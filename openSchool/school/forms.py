from django import forms
from .models import ExtendUser, Course

class SignInForm(forms.ModelForm):
    class Meta():
        model = ExtendUser
        fields = ('username','email','password','profile',)

        widgets = {
            'username':forms.TextInput(attrs = {'class':'formInput'}),
            'email': forms.EmailInput(attrs = {'class':'formInput'}),
            'password':forms.PasswordInput(attrs = {'class': 'formInput'}),
            'profile':forms
        }
