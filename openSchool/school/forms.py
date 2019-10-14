from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import ExtendUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username','email','password1','password2',)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class LoginForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username','email','password1','password2',)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class EditProfileForm(forms.ModelForm):
    profile = forms.ImageField()
    class Meta:
        model = ExtendUser
        fields = (
            'userKey',
            'profile',
        )
    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)

        if commit:
            user.save()

        return user