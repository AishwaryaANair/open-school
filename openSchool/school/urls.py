from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from .import views

urlpatterns = [
    path('signIn.html',views.signIn,name ='signIn'),
    path('login.html',views.loginView,name ='login'),
    #path('signup',views.signup,name='signup'),
    path('',views.home,name='home'),  
    path('signupnext.html',views.SignUpNext,name='SignUpNext'),
    path('signlast.html',views.SignInLast,name='SignLast'),

]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
