from django.shortcuts import render
from django.shortcuts import render
from .models import *

# Create your views here.

def login(request):
    return render(request,'/login.html')

def signup(request):
    return render(request,'/signIn.html')

def home(request):
    return render(request,'home.html')
