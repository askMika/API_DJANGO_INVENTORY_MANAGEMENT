from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('learner', 'Learner'),
        ('librarian', 'Librarian'),
        ('cook', 'Cook'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
    
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
 
    

class LearnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
 

class CookProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
  

class LibrarianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   

