from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import ExtendUser, Course


#Sign In Main

def signIn(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('SignUpNext')
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            instruct = ExtendUser.objects.get(userKey = request.user)
            if instruct.isInstructor:
                return redirect('instructorDash')
            else:
                return redirect('checkProgress')
        else:
            # Return an 'invalid login' error message.
            args = {'form': form}
            return render(request, 'login.html', args)
    else:
            # Return an 'invalid login' error message.
            form = AuthenticationForm(data = request.POST)
            args = {'form': form}
            return render(request, 'login.html', args)

def SignUpNext(request):

    #Profile photo upload -does not work yet
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        val = request.POST['isStudent']
        if form.is_valid():
            obj = User.objects.filter().order_by('-id')[0]
            userObject = ExtendUser.objects.create(userKey = obj)
            userObject.profile = form.cleaned_data['profile']
            if val == 'Student':
                userObject.isStudent = True
                userObject.isInstructor = False
                userObject.save()
                return redirect('home')
            else:
                userObject.isStudent = False
                userObject.isInstructor = True
                userObject.save()
                return redirect('home')
            
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

@login_required()
def checkProgress(request):
    #Check Progress Tab
    return render(request, 'courseprogress.html')

@login_required()
def instructorDash(request):
    #Instructor Dashboard
    user = request.user
    coursesCreated = Course.objects.filter(creator=request.user)
    template = 'instructor.html'
    return render(request, template, {'coursesCreated':coursesCreated,'user': user})

@login_required()
def courseEdit(request):
    #Edit Course Content
    if request.method == 'POST':
        pass
    else:
        form = AddCourseForm()
        args = {'course': request.newWeek, 'form':  form }
        return render(request, 'courseedit.html', args)


@login_required()
def courseAdd(request):
    #Add a course
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid:
            newCourse = Course.objects.create(creator = request.user)
            newCourse.courseTitle = request.POST['courseTitle']
            newCourse.courseDescription = request.POST['courseDescription']
            newCourse.hours = int(request.POST['hours'])
            newCourse.save()
            return render(request, 'courseedit.html', {'course':newCourse,'user': request.user})
        '''else:
            form = AddCourseForm()
            args = {}
            args['creator'] = request.user
            args['form'] = form
            return render(request, 'addcourse.html', args)
        '''
    else:
        form = AddCourseForm()
        args = {}
        args['creator'] = request.user
        args['form'] = form
        return render(request, 'addcourse.html', args)
    

@login_required()
def logoutRequest(request):
    logout(request)
    return redirect("home")