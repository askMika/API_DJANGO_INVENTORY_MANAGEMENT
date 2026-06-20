from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (InventorymanagementProduct, InventorymanagementBookproduct, InventorymanagementFoodproduct, InventorymanagementStationeryproduct, InventorymanagementTextbookproduct, InventorymanagementStockitem,InventorymanagementBookstockitem,
                      InventorymanagementFoodstockitem,InventorymanagementStationerystockitem,InventorymanagementTextbookstockitem)

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
#  List all & Create 
class ProductListView(APIView):

    # READ ALL (Updated to pull base data cleanly!)
    def get(self, request):
        # 1. Fetch records straight from the base product table
        products = InventorymanagementProduct.objects.all()
        
        # 2. Serialize them using the base ProductSerializer 
        serializer = ProductSerializer(products, many=True)
        
        # 3. Return the clean array data to your frontend fetch call
        return Response(serializer.data)

#  Get one, Update & Delete 
class ProductDetailView(APIView):

    # helper — find product or return 404
    def get_object(self, pk):
        try:
            return InventorymanagementProduct.objects.get(pk=pk)
                
        except InventorymanagementProduct.DoesNotExist:
            return None

    # READ ONE
    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {"error": "Product not found."},

            )
        # pick the right serializer based on product type
        product_type = product.__class__.__name__.lower().replace('product', '')
        SerializerClass, _ = SERIALIZER_MAP.get(product_type, (ProductSerializer, None))
        serializer = SerializerClass(product)
        return Response(serializer.data)

    # UPDATE
    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {"error": "Product not found."},

            )
        product_type = product.__class__.__name__.lower().replace('product', '')
        SerializerClass, _ = SERIALIZER_MAP.get(product_type, (ProductSerializer, None))
        serializer = SerializerClass(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # PARTIAL UPDATE
    def patch(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {"error": "Product not found."},

            )
        product_type = product.__class__.__name__.lower().replace('product', '')
        SerializerClass, _ = SERIALIZER_MAP.get(product_type, (ProductSerializer, None))
        serializer = SerializerClass(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {"error": "Product not found."},
            )
        product.delete()
        return Response(
            {"message": "Product deleted successfully."},
        )
    
class StockItemListView(APIView):

    def get(self, request):
        items = InventorymanagementStockitem.objects.all()
        serializer = StockItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):

        item_type = request.data.get('item_type')

        if item_type not in STOCK_SERIALIZER_MAP:
            return Response(
                {"error": "Invalid item_type"},
            )

        SerializerClass, _ = STOCK_SERIALIZER_MAP[item_type]

        serializer = SerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

class StockItemDetailView(APIView):

    def get_object(self, pk):
        try:
            return InventorymanagementStockitem.objects.get(pk=pk)
        except InventorymanagementStockitem.DoesNotExist:
            return None      
        
    # READ ONE
    def get(self, request, pk):
        StockItem = self.get_object(pk)
        if not StockItem:
            return Response(
                {"error": "item not found."},
            )
        # pick the right serializer based on item type
        item_type = StockItem.__class__.__name__.lower().replace('item', '')
        SerializerClass, _ = STOCK_SERIALIZER_MAP.get(item_type, (StockItemSerializer, None))
        serializer = SerializerClass(StockItem)
        return Response(serializer.data)

    # UPDATE
    def put(self, request, pk):
        StockItem = self.get_object(pk)
        if not StockItem:
            return Response(
                {"error": "Product not found."},
            )
        item_type = StockItem.__class__.__name__.lower().replace('item', '')
        SerializerClass, _ = STOCK_SERIALIZER_MAP.get(item_type, (StockItemSerializer, None))
        serializer = SerializerClass(StockItem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # PARTIAL UPDATE
    def patch(self, request, pk):
        StockItem = self.get_object(pk)
        if not StockItem:
            return Response(
                {"error": "Product not found."},
            )
        item_type = StockItem.__class__.__name__.lower().replace('item', '')
        SerializerClass, _ = STOCK_SERIALIZER_MAP.get(item_type, (StockItemSerializer, None))
        serializer = SerializerClass(StockItem, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # DELETE
    def delete(self, request, pk):
        StockItem = self.get_object(pk)
        if not StockItem:
            return Response(
                {"error": "Product not found."},
             
            )
        StockItem.delete()
     
        return Response(
            {"message": "Product deleted successfully."},
    
        )    