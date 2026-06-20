from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'users'

class TeacherProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, models.CASCADE)

    class Meta:
        db_table = 'authentication_teacherprofile'

class LearnerProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, models.CASCADE)

    class Meta:
        db_table = 'authentication_learnerprofile'

class CookProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, models.CASCADE)

    class Meta:
        db_table = 'authentication_cookprofile'

class LibrarianProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, models.CASCADE)

    class Meta:
        db_table = 'authentication_librarianprofile'