from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class LoginForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','password')

    def save(self, commit=True):
        user = super(LoginForm, self).save(commit=False)

        if commit:
            user.save()

        return user

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'email',
            'comments',
        )

    def save(self, commit=True):
        content = super(ContactForm, self).save(commit=False)

        if commit:
            content.save()

        return content

class EditProfileForm(forms.ModelForm):
    profile = forms.ImageField()
    class Meta:
        model = ExtendUser
        fields = (
            'profile',
            'isStudent',
            'isInstructor'
        )
    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)

        if commit:
            user.save()

        return user

class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            'courseTitle',
            'courseDescription',
            'hours',
            'creator'
        )

    def save(self, commit=True):
        course = super(AddCourseForm, self).save(commit=False)

        if commit:
            course.save()

        return course

class AddContentForm(forms.ModelForm):
    weekVideo = forms.FileField()
    class Meta:
        model = Weeks
        fields = (
            'weekTitle',
            'weekVideo',
            'weekDesc',
        )

    def save(self, commit=True):
        content = super(AddContentForm, self).save(commit=False)

        if commit:
            content.save()

        return content

class EditContentForm(forms.ModelForm):
    weekVideo = forms.FileField(required = False)
    weekTitle = forms.CharField(required = False)
    weekDesc = forms.CharField(required = False)
    class Meta:
        model = Weeks
        fields = (
            'weekTitle',
            'weekVideo',
            'weekDesc',
        )

    def save(self, commit=True):
        content = super(AddContentForm, self).save(commit=False)

        if commit:
            content.save()

        return content
