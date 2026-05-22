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
# library/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookBorrowedSerializer
from .service import borrow_book

class BorrowBookView(APIView):
    def post(self, request, pk):
        learner_id = request.data.get("learner_id")
        librarian_id = request.data.get("librarian_id")

        try:
            record = borrow_book(pk, learner_id, librarian_id)
            serializer = BookBorrowedSerializer(record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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


