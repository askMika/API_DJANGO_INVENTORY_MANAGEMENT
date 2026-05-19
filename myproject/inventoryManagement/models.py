import uuid
import qrcode
from io import BytesIO
from django.db import models
from django.core.files import File
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
    @property
    def quantity(self):
         return StockItem.objects.filter(product=self).count()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    qr_code     = models.ImageField(upload_to='qr_codes/products/', blank=True, null=True)

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
    expiry_date   = models.DateField()
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

    class Meta:
        verbose_name        = "Textbook"
        verbose_name_plural = "Textbooks"



# BASE STOCK ITEM  (Polymorphic hierarchy)
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

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.quantity = StockItem.objects.filter(
            product=self.product
        ).count()
        self.product.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.product.quantity = StockItem.objects.filter(
            product=self.product
        ).count()
        self.product.save()

    qr_code    = models.ImageField(upload_to='qr_codes/stock/', blank=True, null=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    condition  = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    added_at   = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes      = models.TextField(blank=True)

    def __str__(self):
        return f"{self.product.name} — Item #{self.id} ({self.status})"
    

    def generate_qr_code(self):
        data = (
            f"Item ID: {self.id}\n"
            f"Product: {self.product.name}\n"
            f"Type: {self.__class__.__name__}\n"
            f"Status: {self.status}\n"
            f"Condition: {self.condition}"
        )
        filename = f"stock_{self.__class__.__name__}_{self.id}.png"
        self.qr_code.save(filename, generate_qr(data, filename), save=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()
            super().save(*args, **kwargs)

    class Meta:
        verbose_name        = "Stock Item"
        verbose_name_plural = "Stock Items"
        ordering            = ['product', 'id']


#─────────────────────────────────────────────────────────────────────
# STOCK ITEM TYPES  (hierarchy)

class StationeryStockItem(StockItem):
    colour   = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(default=1)    # e.g. a pack of 10 pens

    class Meta:
        verbose_name        = "Stationery Stock Item"
        verbose_name_plural = "Stationery Stock Items"


class FoodStockItem(StockItem):
    expiry_date  = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    weight_kg    = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    class Meta:
        verbose_name        = "Food Stock Item"
        verbose_name_plural = "Food Stock Items"


class BookStockItem(StockItem):
    copy_number  = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name        = "Book Stock Item"
        verbose_name_plural = "Book Stock Items"


class TextbookStockItem(StockItem):
    copy_number    = models.IntegerField(default=1)
    issued_to      = models.CharField(max_length=200, blank=True)   # learner name
    is_available   = models.BooleanField(default=True)
    return_date    = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name        = "Textbook Stock Item"
        verbose_name_plural = "Textbook Stock Items"


class OtherStockItem(StockItem):
    """
    For any unknown or uncategorised items that need to be stored.
    """
    item_type    = models.CharField(max_length=100, blank=True)   # user defined type
    serial_number= models.CharField(max_length=100, blank=True)
    location     = models.CharField(max_length=100, blank=True)   # where it is stored

    class Meta:
        verbose_name        = "Other Stock Item"
        verbose_name_plural = "Other Stock Items"