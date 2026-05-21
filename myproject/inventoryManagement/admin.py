from django.contrib import admin
from django.utils.html import format_html
from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
)
from .models import (
    Product, StationeryProduct, FoodProduct, BookProduct, TextbookProduct,
    StockItem, StationeryStockItem, FoodStockItem, BookStockItem,
    TextbookStockItem,
)
# IMAGE PREVIEW HELPER
def image_preview(obj):
    if obj.image:
        return format_html(
            '<img src="{}" width="80" height="80" style="border-radius:4px; object-fit:cover;" />',
            obj.image.url
        )
    return "—"
image_preview.short_description = "Cover"


# QR CODE PREVIEW HELPER
def qr_preview(obj):
    if obj.qr_code:
        return format_html(
            '<img src="{}" width="80" height="80" style="border-radius:4px;" />',
            obj.qr_code.url
        )
    return "—"
qr_preview.short_description = "QR Code"


# STOCK ITEM INLINES
class StationeryStockItemInline(admin.TabularInline):
    model  = StationeryStockItem
    extra  = 1
    fields = ['status', 'condition', 'colour', 'quantity', 'notes']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = StationeryProduct.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FoodStockItemInline(admin.TabularInline):
    model  = FoodStockItem
    extra  = 1
    fields = ['status', 'condition', 'expiry_date', 'batch_number', 'weight_kg', 'notes']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = FoodProduct.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BookStockItemInline(admin.TabularInline):
    model  = BookStockItem
    extra  = 1
    fields = ['status', 'condition', 'copy_number', 'is_available', 'notes']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = BookProduct.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TextbookStockItemInline(admin.TabularInline):
    model  = TextbookStockItem
    extra  = 1
    fields = ['status', 'condition', 'copy_number', 'issued_to', 'is_available', 'return_date', 'notes']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = TextbookProduct.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# PRODUCT CHILD ADMINS
@admin.register(StationeryProduct)
class StationeryProductAdmin(PolymorphicChildModelAdmin):
    base_model      = StationeryProduct
    inlines         = [StationeryStockItemInline]
    list_display    = ['name', 'brand', 'category', 'colour', 'price', 'quantity', qr_preview]
    search_fields   = ['name', 'brand']
    list_filter     = ['category', 'colour', 'brand']
    readonly_fields = ['quantity', 'qr_code', qr_preview]

    fieldsets = (
        ("Product Info",    {"fields": ("name", "description", "price", "quantity")}),
        ("Stationery Info", {"fields": ("brand", "colour", "category")}),
        ("QR Code",         {"fields": ("qr_code", qr_preview)}),
    )


@admin.register(FoodProduct)
class FoodProductAdmin(PolymorphicChildModelAdmin):
    base_model      = FoodProduct
    inlines         = [FoodStockItemInline]
    list_display    = ['name', 'supplier', 'expiry_date', 'storage_temp', 'price', 'quantity', qr_preview]
    search_fields   = ['name', 'supplier']
    list_filter     = ['is_perishable', 'storage_temp']
    readonly_fields = ['quantity', 'qr_code', qr_preview]

    fieldsets = (
        ("Product Info", {"fields": ("name", "description", "price", "quantity")}),
        ("Food Info",    {"fields": ("supplier", "expiry_date", "is_perishable", "storage_temp", "weight_kg")}),
        ("QR Code",      {"fields": ("qr_code", qr_preview)}),
    )



@admin.register(BookProduct)
class BookProductAdmin(PolymorphicChildModelAdmin):
    base_model      = BookProduct
    inlines         = [BookStockItemInline]
    list_display    = ['name', 'author', 'genre', 'publisher', 'price', 'quantity', image_preview, qr_preview]
    search_fields   = ['name', 'author', 'isbn']
    list_filter     = ['genre', 'language']
    readonly_fields = ['quantity', 'qr_code', qr_preview, image_preview]

    fieldsets = (
        ("Product Info", {"fields": ("name", "description", "price", "quantity")}),
        ("Book Info",    {"fields": ("author", "isbn", "publisher", "genre", "published_year", "language", "pages")}),
        ("Cover Image",  {"fields": ("image", image_preview)}),
        ("QR Code",      {"fields": ("qr_code", qr_preview)}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = BookProduct.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(TextbookProduct)
class TextbookProductAdmin(PolymorphicChildModelAdmin):
    base_model      = TextbookProduct
    inlines         = [TextbookStockItemInline]
    list_display    = ['name', 'author', 'subject', 'grade', 'curriculum', 'price', 'quantity', image_preview, qr_preview]
    search_fields   = ['name', 'author', 'subject', 'isbn']
    list_filter     = ['grade', 'subject', 'curriculum']
    readonly_fields = ['quantity', 'qr_code', qr_preview, image_preview]

    fieldsets = (
        ("Product Info",  {"fields": ("name", "description", "price", "quantity")}),
        ("Textbook Info", {"fields": ("author", "isbn", "publisher", "subject", "grade", "edition", "published_year", "curriculum")}),
        ("Cover Image",   {"fields": ("image", image_preview)}),
        ("QR Code",       {"fields": ("qr_code", qr_preview)}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = TextbookProduct.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
# PRODUCT PARENT ADMIN
@admin.register(Product)
class ProductAdmin(PolymorphicParentModelAdmin):
    base_model      = Product
    list_display    = ['name', 'price', 'quantity', 'created_at', 'polymorphic_ctype', qr_preview]
    list_filter     = [PolymorphicChildModelFilter]
    search_fields   = ['name']
    readonly_fields = ['quantity', qr_preview]
    child_models    = [
        StationeryProduct,
        FoodProduct,
        BookProduct,
        TextbookProduct,
    ]


# STOCK ITEM CHILD ADMINS
@admin.register(StationeryStockItem)
class StationeryStockItemAdmin(PolymorphicChildModelAdmin):
    base_model      = StationeryStockItem
    list_display    = ['id', 'product', 'colour', 'quantity', 'status', 'condition', qr_preview]
    list_filter     = ['status', 'condition']
    search_fields   = ['product__name', 'colour']
    readonly_fields = ['qr_code', qr_preview, 'added_at', 'updated_at']

    fieldsets = (
        ("Item Info",       {"fields": ("product", "status", "condition")}),
        ("Stationery Info", {"fields": ("colour", "quantity")}),
        ("Notes",           {"fields": ("notes",)}),
        ("QR Code",         {"fields": ("qr_code", qr_preview)}),
        ("Timestamps",      {"fields": ("added_at", "updated_at")}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = StationeryProduct.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(FoodStockItem)
class FoodStockItemAdmin(PolymorphicChildModelAdmin):
    base_model      = FoodStockItem
    list_display    = ['id', 'product', 'batch_number', 'expiry_date', 'status', 'condition', qr_preview]
    list_filter     = ['status', 'condition']
    search_fields   = ['product__name', 'batch_number']
    readonly_fields = ['qr_code', qr_preview, 'added_at', 'updated_at']

    fieldsets = (
        ("Item Info",  {"fields": ("product", "status", "condition")}),
        ("Food Info",  {"fields": ("expiry_date", "batch_number", "weight_kg")}),
        ("Notes",      {"fields": ("notes",)}),
        ("QR Code",    {"fields": ("qr_code", qr_preview)}),
        ("Timestamps", {"fields": ("added_at", "updated_at")}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = FoodProduct.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(BookStockItem)
class BookStockItemAdmin(PolymorphicChildModelAdmin):
    base_model      = BookStockItem
    list_display    = ['id', 'product', 'copy_number', 'is_available', 'status', 'condition', qr_preview]
    list_filter     = ['status', 'condition', 'is_available']
    search_fields   = ['product__name']
    readonly_fields = ['qr_code', qr_preview, 'added_at', 'updated_at']

    fieldsets = (
        ("Item Info",  {"fields": ("product", "status", "condition")}),
        ("Book Info",  {"fields": ("copy_number", "is_available")}),
        ("Notes",      {"fields": ("notes",)}),
        ("QR Code",    {"fields": ("qr_code", qr_preview)}),
        ("Timestamps", {"fields": ("added_at", "updated_at")}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = BookProduct.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(TextbookStockItem)
class TextbookStockItemAdmin(PolymorphicChildModelAdmin):
    base_model      = TextbookStockItem
    list_display    = ['id', 'product', 'copy_number', 'issued_to', 'is_available', 'return_date', 'status', qr_preview]
    list_filter     = ['status', 'condition', 'is_available']
    search_fields   = ['product__name', 'issued_to']
    readonly_fields = ['qr_code', qr_preview, 'added_at', 'updated_at']

    fieldsets = (
        ("Item Info",     {"fields": ("product", "status", "condition")}),
        ("Textbook Info", {"fields": ("copy_number", "issued_to", "is_available", "return_date")}),
        ("Notes",         {"fields": ("notes",)}),
        ("QR Code",       {"fields": ("qr_code", qr_preview)}),
        ("Timestamps",    {"fields": ("added_at", "updated_at")}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = TextbookProduct.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# STOCK ITEM PARENT ADMIN
@admin.register(StockItem)
class StockItemAdmin(PolymorphicParentModelAdmin):
    base_model      = StockItem
    list_display    = ['id', 'status', 'condition', 'added_at', 'polymorphic_ctype', qr_preview]
    list_filter     = [PolymorphicChildModelFilter, 'status', 'condition']
    search_fields   = []
    readonly_fields = [qr_preview]
    child_models    = [
        StationeryStockItem,
        FoodStockItem,
        BookStockItem,
        TextbookStockItem,
    ]