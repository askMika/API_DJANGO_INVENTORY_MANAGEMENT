from rest_framework import serializers
from .models import BorrowedBook  # Fixed: Changed from BorrowedBooks to BorrowedBook

class BorrowedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook  # Fixed: Points to the updated singular model class
        fields = '__all__'