from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class ExtendUser(models.Model):
    userKey = models.OneToOneField(User,on_delete=models.CASCADE)
    profile = models.ImageField(upload_to = 'images', default = 'images/no-img.jpg')
    isInstructor = models.BooleanField(default = False)

class Course(models.Model):
    courseTitle = models.TextField(max_length = 200)
    courseDescription = models.TextField(max_length = 500)
    hours = models.IntegerField(default = 200)
    creator = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='UserCreator')
    userMap = models.ManyToManyField('auth.User',related_name='LearnersEnrolled')


class Weeks(models.Model):
    weekTitle = models.TextField(max_length = 100)
    courseDet = models.ForeignKey('school.Course',on_delete=models.CASCADE)
    weekVideo = models.FileField(upload_to='videos/', null=True, verbose_name="")
    #weekQuiz = models.ForeignKey('school.ModuleTest',on_delete=models.CASCADE)

'''
class ModuleTest(models.Model):
    

class Results(models.Model):
    pass
'''