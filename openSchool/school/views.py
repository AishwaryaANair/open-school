from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


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
    course = Course.objects.filter().order_by('-id')[0]
    args = {'courses': course }
    return render(request,'brocode.html',args)

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
            if instruct == None:
                args = {'form': form}
                return render(request, 'login.html', args)
            elif instruct.isInstructor:
                return redirect('instructorDash')
            else:
                return render(request, 'learner.html')
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
def instructorDash(request):
    #Instructor Dashboard
    user = request.user
    coursesCreated = Course.objects.filter(creator=request.user)
    template = 'instructor.html'
    return render(request, template, {'coursesCreated':coursesCreated,'user': user})

@login_required()
def courseEdit(request, courseUID):
    #Edit Course Content
    course = get_object_or_404(Course, pk=courseUID)
    try:
        weeksCreated = Weeks.objects.filter(courseDet = course)
    except Weeks.DoesNotExist:
        weeksCreated = None
    finally:
        return render(request, 'courseedit.html', {'newWeek':weeksCreated, 'course': course})
    
@login_required()
def editWeekContent(request, weekUID):
    #Edit Course Content
    week = Weeks.objects.get(pk = weekUID)
    if request.method == 'POST':
        form = AddContentForm(request.POST)
        if form.is_valid:
            week.weekTitle = form.cleaned_data['weekTitle']
            week.weekDesc = form.cleaned_data['weekDesc']
            week.weekVideo = form.cleaned_data['weekVideo']
            week.save()
            return redirect('updatedCourse', courseID = week.courseDet)
    else:
        return render(request, 'editweekcontent.html', {'newWeek':week})

@login_required()
def updatedView(request, courseID):
    #updating the courses
    courseObj = Course.objects.filter(pk = courseID)
    weeksCreated = Weeks.objects.filter(courseDet = courseID)
    template = 'courseedit.html'
    args = {'course': courseObj, 'newWeek':weeksCreated}
    return render(request , template, args)

@login_required()
def addWeekContent(request, courseUID):
    #Add videos to weeks
    course = Course.objects.get(pk = courseUID)
    if request.method == 'POST':
        form = AddContentForm(request.POST, request.FILES)
        if form.is_valid():
            newWeek = Weeks.objects.create(courseDet = course)
            newWeek.weekTitle = form.cleaned_data['weekTitle']
            newWeek.weekDesc = form.cleaned_data['weekDesc']
            newWeek.weekVideo = form.cleaned_data['weekVideo']
            newWeek.save()
            newWeeks = Weeks.objects.filter(courseDet = courseUID)
            return redirect('updatedCourse', courseID = courseUID)
            
    else:
        form = AddContentForm()
        args = {}
        args['course'] = course
        args['form'] = form
        args['newWeek'] = None
        return render(request, 'addweekcontent.html',args)
    #, {'newWeek':weeksCreated,'course': courseName})


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
            return render(request, 'courseedit.html', {'course': newCourse,'user': request.user})
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

def courseView(request):
    return (request, 'courseview.html', {'course': request.course, 'user': request.user})

@login_required()
def logoutRequest(request):
    logout(request)
    return redirect("home")


@login_required()
def learner(request):
    return render(request,"learner.html")

def courseprogress(request):
    #Check Progress Tab
    return render(request,"courseprogress.html")

def completedcourses(request):
    #Check Progress Tab
    return render(request,"completedcourses.html")

def coursecontent(request):
    #Check Progress Tab
    return render(request,"coursecontent.html")

def coursedetails(request):
    #Check Progress Tab
    return render(request,"coursedetails.html")
