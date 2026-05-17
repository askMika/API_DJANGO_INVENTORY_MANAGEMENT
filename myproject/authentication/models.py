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
    subject = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=20)

class LearnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.IntegerField()
    student_number = models.CharField(max_length=20)

class CookProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kitchen_station = models.CharField(max_length=100)

class LibrarianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    library_section = models.CharField(max_length=100)