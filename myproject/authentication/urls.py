from django.urls import path
from .views import register, check_student_exists  # Imported locally from this app's views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', register),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('students/<str:username>/', check_student_exists, name='check-student'),
]