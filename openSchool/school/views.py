from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponse
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

    form = ContactForm()
    args = {'form': form}
    return render(request, 'contactus.html', args)


def postContact(request):
	if request.method == "POST" and request.is_ajax():
		form = ContactForm(request.POST)
		form.save()
		return JsonResponse({"success":True}, status=200)
	return JsonResponse({"success":False}, status=400)

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
            Student = ExtendUser.objects.get(userKey = request.user)
            if instruct == None:
                args = {'form': form}
                return render(request, 'login.html', args)
            elif instruct.isInstructor:
                arg = {'instruct':instruct}
                return redirect('instructorDash')
            elif Student.isStudent:
                arg = {'Student':Student}
                return redirect('learner') 
        else:
            # Return an 'invalid login' error message.
            form =  AuthenticationForm()
            message = 'Username and Password do not match'
            args = {'form': form, 'error': message }
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
            if form.cleaned_data['weekVideo']:
                newWeek.weekVideo = form.cleaned_data['weekVideo']
                newWeek.save()
            return redirect('weekedit',weekUID = newWeek.pk)
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

def course(request, courseUID):
    item = get_object_or_404(Course, pk = courseUID)
    return render(request, 'instructor.html',{'course':item})


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
    course = Course.objects.all()
    args = {'course':course}
    return render(request,'learner.html',args)
	
	
def courseprogress(request,courseID):
    #Check Progress Tab
    user = request.user
    Student = ExtendUser.objects.get(userKey = request.user)
    course = Course.objects.get(pk=courseID)
    template = 'courseprogress.html'
    return render(request, template, {'course':course,'user': user, 'Student':Student })

def completedcourses(request):
    #Check Progress Tab
    return render(request,"completedcourses.html")
   
def coursecontent(request,weekUID):
    #Check Progress Tab
    newWeek =  Weeks.objects.get(pk = weekUID)
    course = Course.objects.get(pk = newWeek.courseDet.pk)
    return render(request,"coursecontent.html",{'newWeek':newWeek, 'course':course })


def coursedetails(request,courseID):
    #Check Progress Tab
    course = Course.objects.get(pk=courseID)
    newWeek = Weeks.objects.filter(courseDet = course)
    return render(request, 'coursedetails.html', { 'newWeek': newWeek ,'course': course})
  

def certi(request):
    #Check Progress Tab
    return render(request,"certi.html")
