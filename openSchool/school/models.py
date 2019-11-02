from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class ExtendUser(models.Model):

    #Profile Photo Model - not functioning yet
    userKey = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to = 'images', default = 'images/no-img.jpg')
    isStudent = models.BooleanField('Student',default = False)
    isInstructor = models.BooleanField('Instructor',default = False)

    def __str__(self):
        return self.userKey.username

class Course(models.Model):
    
    #Course model
    
    courseTitle = models.TextField(max_length = 200)
    courseDescription = models.TextField(max_length = 500)
    hours = models.IntegerField(default = 112)
    creator = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='UserCreator')
    userMap = models.ManyToManyField('auth.User',related_name='LearnersEnrolled', null = True)

    objects = models.Manager()    

    def get_absolute_url(self):
        return reverse('course', args=[str(self.pk)])
    
    def __str__(self):
        return self.courseTitle

class Weeks(models.Model):

    #Weeks added
    weekTitle = models.TextField(max_length = 100)
    courseDet = models.ForeignKey('school.Course',on_delete=models.CASCADE)
    weekVideo = models.FileField(upload_to='videos/', null=True, verbose_name="")
    weekDesc = models.TextField(max_length = 200)
    #weekQuiz = models.ForeignKey('school.ModuleTest',on_delete=models.CASCADE)

    def __str__(self):
        return self.weekTitle

class Contact(models.Model):
    email = models.CharField(max_length = 100)
    comments = models.TextField(max_length = 500)

    def __str__(self):
        return self.email