# library/admin.py
from django.contrib import admin
from .models import BookBorrowed,Bill


@admin.register(BookBorrowed)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ("book_item", "learner", "librarian", "borrowed_at", "returned_at")
    list_filter = ("borrowed_at", "returned_at", "librarian")
    search_fields = ("book_item__product__name", "learner__user__username", "librarian__user__username")

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("learner", "total_amount", "lost_books", "late_returns")
    search_fields = ("learner__user__username",)

    from django.contrib import admin
from .models import BookStockItem
