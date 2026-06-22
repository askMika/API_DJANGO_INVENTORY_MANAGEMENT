from django.db import models

class InventorymanagementProduct(models.Model):
    # Django auto-generates 'id' as a SERIAL PRIMARY KEY by default if not specified,
    # but since you are using an existing legacy/inspectdb table layout:
    id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    qty = models.IntegerField(default=0, blank=True, null=True)
    received = models.DateField(blank=True, null=True)  # Using DateField for raw tracking
    supplier = models.CharField(max_length=255, blank=True, null=True)
    condition = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    # Text or URL fields to store links/paths to the images and QR codes
    image = models.TextField(blank=True, null=True)     
    qrcode = models.TextField(blank=True, null=True)    

    class Meta:
        db_table = 'inventorymanagement_product'  # Forces Django to target your exact SQL tabl

class InventorymanagementBookproduct(models.Model):
    product_ptr = models.OneToOneField(InventorymanagementProduct, models.CASCADE, primary_key=True)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20)
    publisher = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)
    published_year = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=50)
    pages = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'book'

class InventorymanagementFoodproduct(models.Model):
    product_ptr = models.OneToOneField(InventorymanagementProduct, models.CASCADE, primary_key=True)
    expiry_date = models.DateField(blank=True, null=True)
    supplier = models.CharField(max_length=100)
    is_perishable = models.BooleanField()
    storage_temp = models.CharField(max_length=20)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)

    class Meta:
        db_table = 'inventoryManagement_foodproduct'

class InventorymanagementStationeryproduct(models.Model):
    product_ptr = models.OneToOneField(InventorymanagementProduct, models.CASCADE, primary_key=True)
    brand = models.CharField(max_length=100)
    colour = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    class Meta:
        db_table = 'inventoryManagement_stationeryproduct'

class InventorymanagementTextbookproduct(models.Model):
    product_ptr = models.OneToOneField(InventorymanagementProduct, models.CASCADE, primary_key=True)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20)
    publisher = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    edition = models.CharField(max_length=50)
    published_year = models.IntegerField(blank=True, null=True)
    curriculum = models.CharField(max_length=50)
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'inventoryManagement_textbookproduct'

class InventorymanagementStockitem(models.Model):
    id = models.BigAutoField(primary_key=True)
    qr_code = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20)
    condition = models.CharField(max_length=20)
    added_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField()

    class Meta:
        db_table = 'inventoryManagement_stockitem'

class InventorymanagementBookstockitem(models.Model):
    stockitem_ptr = models.OneToOneField(InventorymanagementStockitem, models.CASCADE, primary_key=True)
    copy_number = models.IntegerField()
    is_available = models.BooleanField()
    product = models.ForeignKey(InventorymanagementBookproduct, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'inventoryManagement_bookstockitem'

class InventorymanagementFoodstockitem(models.Model):
    stockitem_ptr = models.OneToOneField(InventorymanagementStockitem, models.CASCADE, primary_key=True)
    expiry_date = models.DateField(blank=True, null=True)
    batch_number = models.CharField(max_length=50)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    product = models.ForeignKey(InventorymanagementFoodproduct, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'inventoryManagement_foodstockitem'

class InventorymanagementStationerystockitem(models.Model):
    stockitem_ptr = models.OneToOneField(InventorymanagementStockitem, models.CASCADE, primary_key=True)
    colour = models.CharField(max_length=50)
    quantity = models.IntegerField()
    product = models.ForeignKey(InventorymanagementStationeryproduct, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'inventoryManagement_stationerystockitem'

class InventorymanagementTextbookstockitem(models.Model):
    stockitem_ptr = models.OneToOneField(InventorymanagementStockitem, models.CASCADE, primary_key=True)
    copy_number = models.IntegerField()
    issued_to = models.CharField(max_length=200)
    is_available = models.BooleanField()
    return_date = models.DateField(blank=True, null=True)
    product = models.ForeignKey(InventorymanagementTextbookproduct, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'inventoryManagement_textbookstockitem'