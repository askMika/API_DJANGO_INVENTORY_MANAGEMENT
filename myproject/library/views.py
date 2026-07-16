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


@api_view(['POST'])
def addBook(request):
    # Extracting exclusively from the React form state payload
    title = request.data.get('title')
    author = request.data.get('author')
    category = request.data.get('category')
    copies = request.data.get('quantity')  # Sent as quantity from React payload
    isbn = request.data.get('isbn')
    shelf = request.data.get('shelf_number')  # Sent as shelf_number from React payload
    image = request.data.get('image')

    with connection.cursor() as cursor:
        sql = """
            INSERT INTO book (
                title, 
                author, 
                category, 
                quantity, 
                isbn, 
                shelf_number, 
                image
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(sql, [title, author, category, copies, isbn, shelf, image])
        new_id = cursor.fetchone()[0]

    # Returning the exact object structural layout expected by the React UI loops
    return Response({
        "id": new_id,
        "title": title,
        "author": author,
        "category": category,
        "copies": copies,
        "isbn": isbn,
        "shelf": shelf,
        "image": image
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def getBookList(request):
   
    list=[]
    with connection.cursor() as cursor:
       sql = """
        SELECT 
            id, 
            title, 
            author, 
            category, 
            quantity, 
            isbn, 
            shelf_number, 
            image,
            COALESCE(available_copies, quantity) AS available
        FROM book
        ORDER BY id DESC;
    """
       
       cursor.execute(sql)
       rows=cursor.fetchall()
       columns = [col[0] for col in cursor.description]
       for row in rows:
           list.append(dict(zip(columns, row)))
    return Response(list, status=status.HTTP_200_OK)
           
    
       
           
        
    
        