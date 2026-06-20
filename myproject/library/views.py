from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BorrowedBooks
from .serializers import BorrowedBooksSerializer
from rest_framework.decorators import api_view

from rest_framework import status


@api_view(['GET'])
def getAll(self,request):
        borrowed_books=BorrowedBooks.objects.all()
        serializer=BorrowedBooksSerializer(borrowed_books,many=True)
        return Response(serializer.data)

@api_view(['POST'])
def addBorrowedBook(self,request):
        serializer=BorrowedBooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)