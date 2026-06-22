from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import BorrowedBook  # Fixed: Changed from BorrowedBooks to BorrowedBook
from .serializers import BorrowedBooksSerializer

@api_view(['GET'])
def getAll(request):  # Fixed: Removed 'self'
    borrowed_books = BorrowedBook.objects.all()
    serializer = BorrowedBooksSerializer(borrowed_books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addBorrowedBook(request):  # Fixed: Removed 'self'
    serializer = BorrowedBooksSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)