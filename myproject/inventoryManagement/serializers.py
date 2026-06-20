from rest_framework import serializers
from .models import (InventorymanagementProduct, InventorymanagementBookproduct, InventorymanagementFoodproduct, InventorymanagementStationeryproduct, InventorymanagementTextbookproduct, InventorymanagementStockitem,InventorymanagementBookstockitem,
                      InventorymanagementFoodstockitem,InventorymanagementStationerystockitem,InventorymanagementTextbookstockitem)


# PRODUCT SERIALIZERS
class StationeryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InventorymanagementStationeryproduct
        fields = '__all__'
        read_only_fields = ['qr_code', 'created_at', 'updated_at']


class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InventorymanagementFoodproduct
        fields = '__all__'
        read_only_fields = ['qr_code', 'created_at', 'updated_at']


class BookProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InventorymanagementBookproduct
        fields = '__all__'
        read_only_fields = ['qr_code', 'created_at', 'updated_at']


class TextbookProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InventorymanagementTextbookproduct
        fields = '__all__'
        read_only_fields = ['qr_code', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    product_type = serializers.SerializerMethodField()

    class Meta:
        model  = InventorymanagementProduct
        fields = '__all__'
        read_only_fields = ['qr_code', 'created_at', 'updated_at']

    def get_product_type(self, obj):
        return obj.__class__.__name__


# STOCK ITEM SERIALIZERS
class StationeryStockItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model  = InventorymanagementStationerystockitem
        fields = '__all__'
        read_only_fields = ['qr_code', 'added_at', 'updated_at']


class FoodStockItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model  = InventorymanagementFoodstockitem
        fields = '__all__'
        read_only_fields = ['qr_code', 'added_at', 'updated_at']


class BookStockItemSerializer(serializers.ModelSerializer):
    product_name  = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model  = InventorymanagementBookstockitem
        fields = '__all__'
        read_only_fields = ['qr_code', 'added_at', 'updated_at']


class TextbookStockItemSerializer(serializers.ModelSerializer):
    product_name  = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model  = InventorymanagementTextbookstockitem
        fields = '__all__'
        read_only_fields = ['qr_code', 'added_at', 'updated_at']



class StockItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    item_type    = serializers.SerializerMethodField()

    class Meta:
        model  = InventorymanagementStockitem
        fields = '__all__'
        
        read_only_fields = ['qr_code', 'added_at', 'updated_at']

    def get_item_type(self, obj):
        return obj.__class__.__name__