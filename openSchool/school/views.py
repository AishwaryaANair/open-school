from django.shortcuts import render
#from .models import ExtendUser,Course, CourseQuiz

# Create your views here.

def signIn(request):
    return render(request,'signIn.html')

def home(request):
    return render(request,'brocode.html')

def login(request):
    return render(request,'loginip.html')

def SignUpNext(request):
    return render(request,'signupnext.html')

def SignUpLast(request):
    return render(request,'signlast.html')

def SignInLast(request):
    return render(request,'signlastinstruct.html')



