# library/models.py
from django.db import models
from django.utils import timezone
from inventoryManagement.models import BookStockItem
from authentication.models import LibrarianProfile, LearnerProfile


class BookBorrowed(models.Model):
    book_item = models.ForeignKey(BookStockItem, on_delete=models.CASCADE, related_name="borrow_records")
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE, related_name="borrowed_books")
    librarian = models.ForeignKey(LibrarianProfile, on_delete=models.CASCADE, related_name="issued_books")
    borrowed_at = models.DateTimeField(default=timezone.now)
    returned_at = models.DateTimeField(null=True, blank=True)

    def mark_returned(self, loan_type="open_shelf"):
        self.returned_at = timezone.now()
        self.book_item.available = True
        self.book_item.save()

        # Calculate late fee
        self.calculate_late_fee(loan_type=loan_type)

        # Update learner's bill
        bill, _ = Bill.objects.get_or_create(learner=self.learner)
        if self.late_fee > 0:
            bill.add_late_fee(self.late_fee)

        self.save()

    def mark_lost(self):
        book_product = self.book_item.product
        replacement_cost = book_product.price + 100.00  # R100 processing
        self.late_fee = replacement_cost

        # Delete stock item
        self.book_item.delete()

        # Update learner's bill
        bill, _ = Bill.objects.get_or_create(learner=self.learner)
        bill.add_lost_book(replacement_cost)

        self.is_lost = True
        self.save()


class Bill(models.Model):
    learner = models.OneToOneField(LearnerProfile, on_delete=models.CASCADE, related_name="bill")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    lost_books = models.PositiveIntegerField(default=0)
    late_returns = models.PositiveIntegerField(default=0)

    def add_late_fee(self, fee):
        self.total_amount += fee
        self.late_returns += 1
        self.save()

    def add_lost_book(self, replacement_cost):
        self.total_amount += replacement_cost
        self.lost_books += 1
        self.save()



