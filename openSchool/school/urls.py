from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from .import views

urlpatterns = [
    path('signIn.html',views.signIn, name ='signIn'),
    path('login.html',views.loginView, name ='login'),
    #path('signup',views.signup,name='signup'),
    path('',views.home, name='home'),  
    path('signupnext.html', views.SignUpNext, name='SignUpNext'),
    path('courseprogress.html', views.checkProgress, name='checkProgress'),
    path('signlast.html',views.SignInLast, name='SignLast'),
    path('instructor.html', views.instructorDash, name='instructorDash'),
    path('home.html', views.logoutRequest, name='logout'),
    path('addcourse.html',views.courseAdd, name = 'addCourse'),
    path('courseedit.html', views.courseEdit, name = 'courseedit')

]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
