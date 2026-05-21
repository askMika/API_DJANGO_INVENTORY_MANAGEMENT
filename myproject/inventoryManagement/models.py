import qrcode
from io import BytesIO
from django.db import models
from django.core.files import File
from django.utils import timezone
from polymorphic.models import PolymorphicModel


# QR CODE HELPER
def generate_qr(data: str, filename: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return File(buffer, name=filename)


# BASE PRODUCT
class Product(PolymorphicModel):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at  = models.DateTimeField(default=timezone.now, null=True, blank=True)
    qr_code     = models.ImageField(upload_to='qr_codes/products/', blank=True, null=True)

    @property
    def quantity(self):
        mgr = getattr(self, 'items', None)
        return mgr.count() if mgr is not None else 0

    quantity.fget.short_description = 'Quantity'

    def __str__(self):
        return self.name

    def generate_qr_code(self):
        data = (
            f"Product: {self.name}\n"
            f"Type: {self.__class__.__name__}\n"
            f"Price: R{self.price}\n"
            f"Quantity: {self.quantity}\n"
            f"ID: {self.id}"
        )
        filename = f"product_{self.id}.png"
        self.qr_code.save(filename, generate_qr(data, filename), save=False)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()
            super().save(*args, **kwargs)


# PRODUCT TYPES

class StationeryProduct(Product):
    brand    = models.CharField(max_length=100, blank=True)
    colour   = models.CharField(max_length=50, blank=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('pen',      'Pen'),
            ('pencil',   'Pencil'),
            ('notebook', 'Notebook'),
            ('ruler',    'Ruler'),
            ('eraser',   'Eraser'),
            ('other',    'Other'),
        ],
        default='other'
    )

    class Meta:
        verbose_name        = "Stationery Product"
        verbose_name_plural = "Stationery Products"


class FoodProduct(Product):
    expiry_date   = models.DateField(null=True, blank=True)
    supplier      = models.CharField(max_length=100, blank=True)
    is_perishable = models.BooleanField(default=True)
    storage_temp  = models.CharField(
        max_length=20,
        choices=[
            ('ambient', 'Ambient (Room Temp)'),
            ('chilled', 'Chilled (2–8°C)'),
            ('frozen',  'Frozen (−18°C)'),
        ],
        default='ambient'
    )
    weight_kg = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    class Meta:
        verbose_name        = "Food Product"
        verbose_name_plural = "Food Products"


class BookProduct(Product):
    author         = models.CharField(max_length=200)
    isbn           = models.CharField(max_length=20, blank=True)
    publisher      = models.CharField(max_length=200, blank=True)
    genre          = models.CharField(
        max_length=50,
        choices=[
            ('fiction',     'Fiction'),
            ('non_fiction', 'Non-Fiction'),
            ('biography',   'Biography'),
            ('science',     'Science'),
            ('history',     'History'),
            ('other',       'Other'),
        ],
        default='other'
    )
    published_year = models.IntegerField(null=True, blank=True)
    language       = models.CharField(max_length=50, default='English')
    pages          = models.IntegerField(null=True, blank=True)
    image          = models.ImageField(upload_to='products/books/', blank=True, null=True)


    class Meta:
        verbose_name        = "Book"
        verbose_name_plural = "Books"


class TextbookProduct(Product):
    author         = models.CharField(max_length=200)
    isbn           = models.CharField(max_length=20, blank=True)
    publisher      = models.CharField(max_length=200, blank=True)
    subject        = models.CharField(max_length=100)
    grade          = models.CharField(
        max_length=20,
        choices=[(f'grade_{i}', f'Grade {i}') for i in range(1, 13)],
        default='grade_1'
    )
    edition        = models.CharField(max_length=50, blank=True)
    published_year = models.IntegerField(null=True, blank=True)
    curriculum     = models.CharField(
        max_length=50,
        choices=[
            ('caps',  'CAPS'),
            ('ieb',   'IEB'),
            ('other', 'Other'),
        ],
        default='caps'
    )
    image          = models.ImageField(upload_to='products/textbooks/', blank=True, null=True)


    class Meta:
        verbose_name        = "Textbook"
        verbose_name_plural = "Textbooks"


# BASE STOCK ITEM
class StockItem(PolymorphicModel):

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed',  'Borrowed'),
        ('reserved',  'Reserved'),
        ('damaged',   'Damaged'),
        ('lost',      'Lost'),
    ]

    CONDITION_CHOICES = [
        ('new',  'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]

    qr_code    = models.ImageField(upload_to='qr_codes/stock/', blank=True, null=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    condition  = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    added_at   = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    notes      = models.TextField(blank=True)

    def __str__(self):
        product = getattr(self, 'product', None)
        name = product.name if product else "Unknown"
        return f"{name} — Item #{self.id} ({self.status})"

    def generate_qr_code(self):
        product = getattr(self, 'product', None)
        product_name = product.name if product else "Unknown"
        data = (
            f"Item ID: {self.id}\n"
            f"Product: {product_name}\n"
            f"Type: {self.__class__.__name__}\n"
            f"Status: {self.status}\n"
            f"Condition: {self.condition}"
        )
        filename = f"stock_{self.__class__.__name__}_{self.id}.png"
        self.qr_code.save(filename, generate_qr(data, filename), save=False)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()
            super().save(*args, **kwargs)

    class Meta:
        verbose_name        = "Stock Item"
        verbose_name_plural = "Stock Items"
        ordering            = ['id']


# STOCK ITEM TYPES

class StationeryStockItem(StockItem):
    product  = models.ForeignKey(StationeryProduct, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    colour   = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name        = "Stationery Stock Item"
        verbose_name_plural = "Stationery Stock Items"


class FoodStockItem(StockItem):
    product      = models.ForeignKey(FoodProduct, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    expiry_date  = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    weight_kg    = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    class Meta:
        verbose_name        = "Food Stock Item"
        verbose_name_plural = "Food Stock Items"


class BookStockItem(StockItem):
    product      = models.ForeignKey(BookProduct, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    copy_number  = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name        = "Book Stock Item"
        verbose_name_plural = "Book Stock Items"


class TextbookStockItem(StockItem):
    product      = models.ForeignKey(TextbookProduct, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    copy_number  = models.IntegerField(default=1)
    issued_to    = models.CharField(max_length=200, blank=True)
    is_available = models.BooleanField(default=True)
    return_date  = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name        = "Textbook Stock Item"
        verbose_name_plural = "Textbook Stock Items"