# library/views.py
from .serializers import BookBorrowedSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from inventoryManagement.models import BookStockItem
from authentication.models import LearnerProfile, LibrarianProfile
from .models import BookBorrowed

from .serializers import BookStockItemSerializer

class BookStockItemListView(APIView):

    def get(self, request):
        items = BookStockItem.objects.all()
        serializer = BookStockItemSerializer(items, many=True)
        return Response(serializer.data)

class BorrowBookView(APIView):
    def post(self, request, pk):
        learner_id = request.data.get("learner_id")
        librarian_id = request.data.get("librarian_id")
        try:
            book_item = BookStockItem.objects.get(pk=pk, available=True)
            learner = LearnerProfile.objects.get(pk=learner_id)
            librarian = LibrarianProfile.objects.get(pk=librarian_id)

            record = BookBorrowed.objects.create(
                book_item=book_item,
                learner=learner,
                librarian=librarian
            )
            book_item.available = False
            book_item.save()

            serializer = BookBorrowedSerializer(record)
            Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReturnBookView(APIView):
    def post(self, request, pk):
        try:
            record = BookBorrowed.objects.get(pk=pk, returned_at__isnull=True)
            record.mark_returned()
            return Response({"message": "Book returned successfully."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


