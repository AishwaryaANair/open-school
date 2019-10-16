from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from .import views

urlpatterns = [
    path('signIn.html',views.signIn, name ='signIn'),
    path('login.html',views.loginView, name ='login'),
    path('', views.home, name='home'),  
    path('signupnext.html', views.SignUpNext, name='SignUpNext'),
    path('courseprogress.html', views.checkProgress, name='checkProgress'),
    path('signlast.html',views.SignInLast, name='SignLast'),
    path('instructor.html', views.instructorDash, name='instructorDash'),
    path('home.html', views.logoutRequest, name='logout'),
    path('addcourse.html',views.courseAdd, name = 'addCourse'),
    path('courseedit.html?courseUID=<int:courseUID>', views.courseEdit, name = 'courseedit'),
    path('addweekcontent.html?courseUID=<int:courseUID>', views.addWeekContent, name = 'addweek'),
    path('editweekcontent.html?weekUID=<int:weekUID>', views.editWeekContent, name = 'weekedit'),
    path('courseview.html?courseUID=<int:courseUID>', views.courseView, name = 'viewcourse'),
    path('updatedcourse?courseID=<int:courseID>', views.updatedView, name = 'updatedCourse'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

