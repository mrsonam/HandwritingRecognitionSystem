from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

# this model is used to save the profile picture of the user
class ProfilePic(models.Model):
    image = models.ImageField(upload_to='profile_pics')

    def __str__(self):
        return f'{"Hello"} ProfilePic'

# this model is used to save the uploaded form
class InputPic(models.Model):
    image = models.ImageField(upload_to='form')

    
    def __str__(self):
        return f'{"Hello"} InputPic'
