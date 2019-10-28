from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from .import views

urlpatterns = [
    #Home Page URLs 
    path('', views.home, name='home'), 

    #Sign In / Login
    path('signIn.html',views.signIn, name ='signIn'),
    path('login.html',views.loginView, name ='login'),
    path('signupnext.html', views.SignUpNext, name='SignUpNext'),

    #Instructor Urls
    path('instructor.html', views.instructorDash, name='instructorDash'),
    path('addcourse.html',views.courseAdd, name = 'addCourse'),
    path('courseedit.html?courseUID=<int:courseUID>', views.courseEdit, name = 'courseedit'),
    path('addweekcontent.html?courseUID=<int:courseUID>', views.addWeekContent, name = 'addweek'),
    path('editweekcontent.html?weekUID=<int:weekUID>', views.editWeekContent, name = 'weekedit'),
    path('courseview.html?courseUID=<int:courseUID>', views.courseView, name = 'viewcourse'),
    path('updatedcourse?courseID=<int:courseID>', views.updatedView, name = 'updatedCourse'),
    
    #Learner Urls
    
    path("learner.html", views.learner, name="learner"),
    path("courseprogress.html", views.courseprogress, name='courseprogress'),
    path("completedcourses.html", views.completedcourses, name='completedcourses'),
    path("coursedetails.html", views.coursedetails, name='coursedetails'),
    path("coursecontent.html", views.coursecontent, name='coursecontent'), 
    path("certi.html", views.certi, name='certi'), 

    #Logout Url

    path('home.html', views.logoutRequest, name='logout'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

