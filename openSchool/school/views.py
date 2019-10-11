from django.shortcuts import render
from django.shortcuts import render
from .models import ExtendUser,Course, CourseQuiz

# Create your views here.

def signIn(request):
    return render(request,'signIn.html')

def home(request):
    return render(request,'home.html')

def login(request):
    return render(request,'loginip.html')
