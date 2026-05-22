# library/services.py
from django.utils import timezone
from inventoryManagement.models import BookStockItem
from authentication.models import LearnerProfile, LibrarianProfile
from .models import BookBorrowed

def borrow_book(book_id: int, learner_id: int, librarian_id: int) -> BookBorrowed:
    """
    Handles borrowing a book:
    - Checks if the book is available
    - Links learner and librarian
    - Creates a borrow record
    - Marks the book as unavailable
    """
    # Get book
    book_item = BookStockItem.objects.get(pk=book_id, is_available=True)

    # Get learner and librarian
    learner = LearnerProfile.objects.get(pk=learner_id)
    librarian = LibrarianProfile.objects.get(pk=librarian_id)

    # Create borrow record
    record = BookBorrowed.objects.create(
        book_item=book_item,
        learner=learner,
        librarian=librarian,
        borrowed_at=timezone.now()
    )

    # Update book availability
    book_item.is_available = False
    book_item.save()

    return record
