from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, EditProfileForm
from .models import ExtendUser


#Sign In Main

def signIn(request):
    if request.method == 'POST':
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

#Home view

def home(request):
    return render(request,'brocode.html')

#Login function

def loginView(request):
    #Login View

    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('checkProgress')
        else:
            args = {'form': form}
            return render(request, 'login.html', args)
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'login.html', args)

#Profile photo upload -does not work yet

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

#Interests Page

def SignUpLast(request):
    return render(request,'signlast.html')

#Instructor Last Page
def SignInLast(request):
    return render(request,'signlastinstruct.html')

@login_required(login_url='/login')
def checkProgress(request):
    #Check Progress Tab
    return render(request,'courseprogress.html')