from rest_framework import serializers
from .models import BookBorrowed, Bill
from inventoryManagement.serializers import BookStockItemSerializer
from authentication.models import LearnerProfile, LibrarianProfile
from inventoryManagement.models import BookStockItem

class BookStockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStockItem
        name = serializers.CharField(source='product.name', read_only=True)
        id = serializers.IntegerField(read_only=True)
  
class BookStockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStockItem
        name = serializers.CharField(source='product.name', read_only=True)
        id = serializers.IntegerField(read_only=True)
  
class BookStockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStockItem
        name = serializers.CharField(source='product.name', read_only=True)
        id = serializers.IntegerField(read_only=True)
  

class BookBorrowedSerializer(serializers.ModelSerializer):
    book_item = BookStockItemSerializer(read_only=True)
    LearnerProfile = serializers.StringRelatedField(read_only=True)
    librarianProfile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BookBorrowed
        fields = [
            "id",
            "book_item",
            "learner",
            "librarian",
            "borrowed_at",
            "due_date",
            "returned_at",
            "is_lost",
            "late_fee",
        ]


class BorrowRecordCreateSerializer(serializers.ModelSerializer):
    """
    For creating borrow records via API.
    Accepts learner_id and librarian_id instead of nested objects.
    """

    learner_id = serializers.PrimaryKeyRelatedField(
        queryset=LearnerProfile.objects.all(), source="learner", write_only=True
    )
    librarian_id = serializers.PrimaryKeyRelatedField(
        queryset=LibrarianProfile.objects.all(), source="librarian", write_only=True
    )

    class Meta:
        model = BookBorrowed
        fields = ["id", "book_item", "learner_id", "librarian_id", "borrowed_at", "due_date"]


class BillSerializer(serializers.ModelSerializer):
    learner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bill
        fields = [
            "id",
            "learner",
            "total_amount",
            "lost_books",
            "damaged_books",
            "late_returns",
        ]
