from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

#Home view

def home(request):
    course = Course.objects.all()[:4]
    args = {'course':course}
    return render(request,'brocode.html',args)

def contact(request):
    
    ''' Contact Us Form Rendering'''

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            args = {'form': form}
            return render(request, 'contactus.html', args)
    else:
        form = ContactForm()
        args = {'form': form}
        return render(request, 'contactus.html', args)

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
                arg = {'instruct':instruct}
                return render(request, 'instructor.html',arg)
            else:
                
                return render(request, 'courseprogress.html')
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

    #Profile photo upload 
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
    instruct = ExtendUser.objects.get(userKey = request.user)
    coursesCreated = Course.objects.filter(creator=request.user)
    template = 'instructor.html'
    return render(request, template, {'coursesCreated':coursesCreated,'user': user,'instruct':instruct})

@login_required()
def courseEdit(request, courseUID):
    #Edit Course Content
    course = get_object_or_404(Course, pk=courseUID)
    instruct = ExtendUser.objects.get(userKey = request.user)
    try:
        weeksCreated = Weeks.objects.filter(courseDet = course)
    except Weeks.DoesNotExist:
        weeksCreated = None
        return render(request, 'courseedit.html', {'newWeek':weeksCreated, 'course': course, 'instruct': instruct})
    else:
        weeksCreated = Weeks.objects.filter(courseDet = course)
        return render(request, 'courseedit.html', {'newWeek':weeksCreated, 'course': course, 'instruct': instruct})
    
@login_required()
def editWeekContent(request, weekUID):
    #Edit Course Content
    newWeek = Weeks.objects.get(pk = weekUID)
    course = Course.objects.get(pk = newWeek.courseDet.pk)
    if request.method == 'POST':
        form = EditContentForm(request.POST, request.FILES)
        if form.is_valid():
            if form.data['weekTitle']:
                newWeek.weekTitle = form.cleaned_data['weekTitle']
                newWeek.save()
            if form.data['weekDesc']:
                newWeek.weekDesc = form.cleaned_data['weekDesc']
                newWeek.save()
            if form.data['weekVideo']:
                newWeek.weekVideo = form.cleaned_data['weekVideo']
                newWeek.save()
            return redirect('courseedit',courseUID = course.pk)
    else:
        form = EditContentForm()
        args = {}
        args['form'] = form
        instruct = ExtendUser.objects.get(userKey = request.user)
        args['instruct'] = instruct
        args['newWeek'] = newWeek
        return render(request, 'editweekcontent.html',args)

@login_required()
def updatedView(request,courseID):
    #updating the courses
    user = request.user
    courseObj = Course.objects.filter(pk = courseID)
    weeksCreated = Weeks.objects.filter(courseDet = courseID)
    template = 'courseedit.html'
    args = {'course': courseObj, 'newWeek':weeksCreated}
    return redirect('courseedit', courseUID = courseID)

@login_required()
def addWeekContent(request, courseUID):
    #Add videos to weeks
    course = Course.objects.get(pk = courseUID)
    instruct = ExtendUser.objects.get(userKey = request.user)
    if request.method == 'POST':
        form = AddContentForm(request.POST, request.FILES)
        if form.is_valid():
            newWeek = Weeks.objects.create(courseDet = course)
            newWeek.weekTitle = form.cleaned_data['weekTitle']
            newWeek.weekDesc = form.cleaned_data['weekDesc']
            newWeek.weekVideo = form.cleaned_data['weekVideo']
            newWeek.save()
            newWeeks = Weeks.objects.filter(courseDet = courseUID)
            return redirect('courseedit', courseUID = courseUID)
            
    else:
        form = AddContentForm()
        args = {}
        args['course'] = course
        args['form'] = form
        instruct = ExtendUser.objects.get(userKey = request.user)
        args['instruct'] = instruct
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
            instruct = ExtendUser.objects.get(userKey = request.user)
            return render(request, 'courseedit.html', {'course': newCourse,'user': request.user,'instruct':instruct})
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
        instruct = ExtendUser.objects.get(userKey = request.user)
        args['form'] = form
        args['instruct'] = instruct
        return render(request, 'addcourse.html', args)

def courseView(request, courseUID):
    course = get_object_or_404(Course, pk=courseUID)
    instruct = ExtendUser.objects.get(userKey = request.user)
    try:
        weeksCreated = Weeks.objects.filter(courseDet = course)
    except Weeks.DoesNotExist:
        weeksCreated = None
        return render(request, 'courseview.html', {'newWeek':weeksCreated, 'course': course, 'instruct': instruct})
    else:
        weeksCreated = Weeks.objects.filter(courseDet = course)
        return render(request, 'courseview.html', {'newWeek':weeksCreated, 'course': course, 'instruct': instruct})

@login_required()
def logoutRequest(request):
    logout(request)
    return redirect("home")

@login_required()
def learner(request):
    data = Course.object.all()
    return render(request,"learner.html",{'data': data})

def courseprogress(request):
    #Check Progress Tab
    title = Course.object.all()
    return render(request,"courseprogress.html",{'title':title})

def completedcourses(request):
    #Check Progress Tab
    return render(request,"completedcourses.html")

def coursecontent(request):
    #Check Progress Tab
    weekTitle=Weeks()
    return render(request,"coursecontent.html")

def coursedetails(request):
    #Check Progress Tab
    return render(request,"coursedetails.html")

def certi(request):
    #Check Progress Tab
    return render(request,"certi.html")
