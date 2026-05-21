from rest_framework import serializers
from .models import (
    Product, StationeryProduct, FoodProduct, BookProduct, TextbookProduct,
    StockItem, StationeryStockItem, FoodStockItem, BookStockItem,
    TextbookStockItem,
)


# PRODUCT SERIALIZERS
class StationeryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StationeryProduct
        fields = [
            'id', 'name', 'description', 'price', 'quantity',
            'brand', 'colour', 'category', 'qr_code',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['qr_code', 'created_at', 'updated_at']


class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FoodProduct
        fields = [
            'id', 'name', 'description', 'price', 'quantity',
            'expiry_date', 'supplier', 'is_perishable',
            'storage_temp', 'weight_kg', 'qr_code',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['qr_code', 'created_at', 'updated_at']


class BookProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BookProduct
        fields = [
            'id', 'name', 'description', 'price', 'quantity',
            'author', 'isbn', 'publisher', 'genre',
            'published_year', 'language', 'pages',
            'image', 'qr_code',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['qr_code', 'created_at', 'updated_at']


class TextbookProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TextbookProduct
        fields = [
            'id', 'name', 'description', 'price', 'quantity',
            'author', 'isbn', 'publisher', 'subject',
            'grade', 'edition', 'published_year', 'curriculum',
            'image', 'qr_code',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['qr_code', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    product_type = serializers.SerializerMethodField()

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'description', 'price',
            'quantity', 'product_type', 'qr_code',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['qr_code', 'created_at', 'updated_at']

    def get_product_type(self, obj):
        return obj.__class__.__name__


# STOCK ITEM SERIALIZERS
class StationeryStockItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model  = StationeryStockItem
        fields = [
            'id', 'product', 'product_name',
            'status', 'condition', 'colour', 'quantity',
            'notes', 'qr_code', 'added_at', 'updated_at',
        ]
        read_only_fields = ['qr_code', 'added_at', 'updated_at']


class FoodStockItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model  = FoodStockItem
        fields = [
            'id', 'product', 'product_name',
            'status', 'condition', 'expiry_date',
            'batch_number', 'weight_kg',
            'notes', 'qr_code', 'added_at', 'updated_at',
        ]
        read_only_fields = ['qr_code', 'added_at', 'updated_at']


class BookStockItemSerializer(serializers.ModelSerializer):
    product_name  = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model  = BookStockItem
        fields = [
            'id', 'product', 'product_name', 'product_image',
            'status', 'condition', 'copy_number', 'is_available',
            'notes', 'qr_code', 'added_at', 'updated_at',
        ]
        read_only_fields = ['qr_code', 'added_at', 'updated_at']


class TextbookStockItemSerializer(serializers.ModelSerializer):
    product_name  = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model  = TextbookStockItem
        fields = [
            'id', 'product', 'product_name', 'product_image',
            'status', 'condition', 'copy_number',
            'issued_to', 'is_available', 'return_date',
            'notes', 'qr_code', 'added_at', 'updated_at',
        ]
        read_only_fields = ['qr_code', 'added_at', 'updated_at']



class StockItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    item_type    = serializers.SerializerMethodField()

    class Meta:
        model  = StockItem
        fields = [
            'id', 'product', 'product_name', 'item_type',
            'status', 'condition', 'notes', 'qr_code',
            'added_at', 'updated_at',
        ]
        read_only_fields = ['qr_code', 'added_at', 'updated_at']

    def get_item_type(self, obj):
        return obj.__class__.__name__