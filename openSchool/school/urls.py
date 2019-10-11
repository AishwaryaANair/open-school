from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('signIn.html',views.signIn,name ='signIn'),
    path('loginip.html',views.login,name ='login'),
    #path('signup',views.signup,name='signup'),
    path('',views.home,name='home'),  

]
