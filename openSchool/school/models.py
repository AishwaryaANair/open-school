from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib import auth
# Create your models here.

class Student(auth.models.User):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    profile = models.ImageField(upload_to = '../media/images', default = '../media/images/no-img.jpg')
    isInstructor = models.BooleanField(default = False)

class Course(models.Model):
    courseTitle = models.TextField(max_length = 200)
    course

class ModuleTest(models.Model):
    pass

class CourseQuiz(models.Model):
    pass

class Results(models.Model):
    pass
