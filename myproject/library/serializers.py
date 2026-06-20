from .models import BorrowedBooks
from rest_framework import serializers

class BorrowedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBooks
        fields = '__all__'  # Automatically captures learner_id, asset_id, loan_period, due_date, librarian_id, status