from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

# Cleaned Imports matching your project tables
from .models import (
    InventorymanagementProduct, 
    InventorymanagementBookproduct, 
    InventorymanagementFoodproduct, 
    InventorymanagementStationeryproduct, 
    InventorymanagementTextbookproduct, 
    InventorymanagementStockitem,
    InventorymanagementBookstockitem,
    InventorymanagementFoodstockitem,
    InventorymanagementStationerystockitem,
    InventorymanagementTextbookstockitem
)

from .serializers import (
    ProductSerializer,
    StationeryProductSerializer,
    FoodProductSerializer,
    BookProductSerializer,
    TextbookProductSerializer,
    StockItemSerializer,
    StationeryStockItemSerializer,
    FoodStockItemSerializer,
    BookStockItemSerializer,
    TextbookStockItemSerializer,
)

SERIALIZER_MAP = {
    'stationery': (StationeryProductSerializer, InventorymanagementStationeryproduct),
    'food':       (FoodProductSerializer, InventorymanagementFoodproduct),
    'book':       (BookProductSerializer, InventorymanagementBookproduct),
    'textbook':   (TextbookProductSerializer, InventorymanagementTextbookproduct),
}

STOCK_SERIALIZER_MAP = {
    'stationery': (StationeryStockItemSerializer, InventorymanagementStationerystockitem),
    'food':       (FoodStockItemSerializer, InventorymanagementFoodstockitem),
    'book':       (BookStockItemSerializer, InventorymanagementBookstockitem),
    'textbook':   (TextbookStockItemSerializer, InventorymanagementTextbookstockitem),
}

# =====================================================================
# PRODUCT VIEWS
# =====================================================================

class ProductListView(APIView):
    def get(self, request):
        products = InventorymanagementProduct.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    def get_object(self, pk):
        try:
            return InventorymanagementProduct.objects.get(pk=pk)
        except InventorymanagementProduct.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        product_type = product.__class__.__name__.lower().replace('product', '')
        SerializerClass, _ = SERIALIZER_MAP.get(product_type, (ProductSerializer, None))
        serializer = SerializerClass(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        product_type = product.__class__.__name__.lower().replace('product', '')
        SerializerClass, _ = SERIALIZER_MAP.get(product_type, (ProductSerializer, None))
        serializer = SerializerClass(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        product_type = product.__class__.__name__.lower().replace('product', '')
        SerializerClass, _ = SERIALIZER_MAP.get(product_type, (ProductSerializer, None))
        serializer = SerializerClass(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({"message": "Product deleted successfully."})

# =====================================================================
# STOCK ITEM VIEWS
# =====================================================================

class StockItemListView(APIView):
    def get(self, request):
        items = InventorymanagementStockitem.objects.all()
        serializer = StockItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        item_type = request.data.get('item_type')
        if item_type not in STOCK_SERIALIZER_MAP:
            return Response({"error": "Invalid item_type"}, status=status.HTTP_400_BAD_REQUEST)
        SerializerClass, _ = STOCK_SERIALIZER_MAP[item_type]
        serializer = SerializerClass(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockItemDetailView(APIView):
    def get_object(self, pk):
        try:
            return InventorymanagementStockitem.objects.get(pk=pk)
        except InventorymanagementStockitem.DoesNotExist:
            return None      
        
    def get(self, request, pk):
        stock_item = self.get_object(pk)
        if not stock_item:
            return Response({"error": "item not found."}, status=status.HTTP_404_NOT_FOUND)
        item_type = stock_item.__class__.__name__.lower().replace('item', '')
        SerializerClass, _ = STOCK_SERIALIZER_MAP.get(item_type, (StockItemSerializer, None))
        serializer = SerializerClass(stock_item)
        return Response(serializer.data)

    def put(self, request, pk):
        stock_item = self.get_object(pk)
        if not stock_item:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        item_type = stock_item.__class__.__name__.lower().replace('item', '')
        SerializerClass, _ = STOCK_SERIALIZER_MAP.get(item_type, (StockItemSerializer, None))
        serializer = SerializerClass(stock_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        stock_item = self.get_object(pk)
        if not stock_item:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        item_type = stock_item.__class__.__name__.lower().replace('item', '')
        SerializerClass, _ = STOCK_SERIALIZER_MAP.get(item_type, (StockItemSerializer, None))
        serializer = SerializerClass(stock_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stock_item = self.get_object(pk)
        if not stock_item:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        stock_item.delete()
        return Response({"message": "Item deleted successfully."})    

# =====================================================================
# STANDALONE FUNCTIONAL VIEWS FOR LIBRARY CHECKOUT SYSTEM
# =====================================================================

from .models import InventorymanagementBookproduct 
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def get_book_by_id(request, pk):
    """
    Fetches raw row parameters directly from the 'book' table via raw SQL.
    Bypasses Django ORM's implicit 'product_ptr_id' column naming checks entirely.
    """
    with connection.cursor() as cursor:
        # Executes direct query using the exact column names visible in pgAdmin
        cursor.execute("SELECT id, title, author, category, isbn FROM book WHERE id = %s", [pk])
        row = cursor.fetchone()
        
    if not row:
        return Response({"error": "Book asset code not found."}, status=status.HTTP_404_NOT_FOUND)
        
    # Maps array indices directly into the expected payload keys
    return Response({
        "id": row[0],
        "title": row[1] or "Untitled Resource",
        "author": row[2] or "Unknown Author",
        "category": row[3] or "General",
        "isbn": row[4] or "N/A"
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def check_book_exists(request, pk):
    """
    Checks for row presence using the exact column structure from your database.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM book WHERE id = %s)", [pk])
        row = cursor.fetchone()
    
    exists = row[0] if row else False
    return Response({"exists": exists}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getBookByISBN(request, isbn):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, author, category, isbn FROM book WHERE isbn = %s",[isbn])
        row=cursor.fetchone()
    if not row:
        return Response({"error": "book not found"},status=status.HTTP_404_NOT_FOUND)
    return Response({"id": row[0],"title": row[1],"author": row[2],"category": row[3],"isbn": row[4]},status=status.HTTP_200_OK)

@api_view(['GET'])
def checkBookExistsByISBN(request, isbn):
    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM book WHERE isbn = %s)",[isbn])
        row = cursor.fetchone();
    
    exists=row[0] if row else False
    return Response({"exists": exists}, status=status.HTTP_200_OK)

@api_view(['POST'])
def addToQueue(request):
    book_isbn=request.data.get('isbn')
    student_username=request.data.get('username')
    added_at=request.data.get('added_at')
    _status=request.data.get('status')

    if not book_isbn or not student_username or not added_at or not _status:
        return Response({"error":"missing fields"},status=status.HTTP_400_BAD_REQUEST)
    
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO book_queue(%s,%s,%s,%s)",[book_isbn],[student_username],[added_at],[_status])
    return Response({""} ,status=status.HTTP_201_CREATED)
