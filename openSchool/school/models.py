from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib import auth
# Create your models here.

class ExtendUser(auth.models.User):
    userKey = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='UserExtend')
    profile = models.ImageField(upload_to = '../media/images', default = '../media/images/no-img.jpg')
    isInstructor = models.BooleanField(default = False)

class Course(models.Model):
    courseTitle = models.TextField(max_length = 200)
    courseDescription = models.TextField(max_length = 500)
    
class Weeks(models.Model):
    pass




class ModuleTest(models.Model):
    pass

class CourseQuiz(models.Model):
    pass

class Results(models.Model):
    pass
