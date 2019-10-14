from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegistrationForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseForbidden
from .models import ExtendUser

from django.contrib.auth.forms import AuthenticationForm

def signIn(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'signupnext.html')
        else:
            args = {'form': form}
            return render(request, 'signIn.html', args)
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'signIn.html', args)

def home(request):
    return render(request,'brocode.html')

def loginView(request):
    if request.method =='POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return render(request,'courseprogress.html')
    else: 
        form = AuthenticationForm()
    return render(request,'login.html',{'form': form})

def SignUpNext(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES,instance=request.user)
        if form.is_valid():
            m = ExtendUser.objects.get(pk = request.User.pk)
            m.profile = form.cleaned_data['profile']
            m.userKey = User.pk
            m.save()
            return render(request, 'login.html')
        else:
            args = {}
            args['userKey'] = request.User
            args['form'] = form
            return render(request, 'signupnext.html', args)
    else:
        form = EditProfileForm()
        args = {}
        args['userKey'] = request.user
        args['form'] = form
        return render(request, 'signupnext.html', args)

def SignUpLast(request):
    return render(request,'signlast.html')

def SignInLast(request):
    return render(request,'signlastinstruct.html')