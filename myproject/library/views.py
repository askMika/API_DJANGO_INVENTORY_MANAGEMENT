from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import BorrowedBook  # Fixed: Changed from BorrowedBooks to BorrowedBook
from .serializers import BorrowedBooksSerializer
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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

@api_view(['GET'])
def getAllBooks(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id , title , author , category , isbn FROM book ORDER BY title ASC")
        data=cursor.fetchall()

    book_list=[]
    for d in data:
        book_list.append({"id": d[0], "title": d[1],"author":d[2], "category" : d[3] , "isbn" : d[4]})

    return Response(book_list,status=status.HTTP_200_OK)

    