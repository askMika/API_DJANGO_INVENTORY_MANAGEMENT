from rest_framework import serializers
from .models import User, TeacherProfile, LearnerProfile, CookProfile, LibrarianProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        # Create user with role
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )

        # Auto-create profile depending on role
        role = validated_data['role']
        if role == 'teacher':
            TeacherProfile.objects.create(user=user)
        elif role == 'learner':
            LearnerProfile.objects.create(user=user)
        elif role == 'cook':
            CookProfile.objects.create(user=user)
        elif role == 'librarian':
            LibrarianProfile.objects.create(user=user)

        return user
