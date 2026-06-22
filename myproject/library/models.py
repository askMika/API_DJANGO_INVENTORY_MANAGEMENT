from django.db import models
from datetime import date

class BorrowedBook(models.Model):
    # Auto-incrementing primary key is handled implicitly by Django as 'id'
    
    learner_username = models.CharField(
        max_length=150, 
        help_text="The username of the student/learner borrowing the item."
    )
    asset_id = models.IntegerField(
        help_text="The asset tracking number linked to the specific physical book unit."
    )
    borrowed_date = models.DateField(
        default=date.today, 
        help_text="The record date indicating when the checkout sequence was committed."
    )
    loan_period = models.DurationField(
        help_text="The time window allocation (stores as a timedelta natively)."
    )
    due_date = models.DateField(
        help_text="The hard calendar expiration date for active possession."
    )
    librarian_username = models.CharField(
        max_length=150, 
        help_text="The username of the logged-in librarian issuing the checkout transaction."
    )
    status = models.CharField(
        max_length=20, 
        default='Active', 
        help_text="Lifecycle state tracking parameter ('Active', 'Returned', 'Overdue')."
    )

    class Meta:
        db_table = 'borrowed_books'
        verbose_name = 'Borrowed Book'
        verbose_name_plural = 'Borrowed Books'

    def __str__(self):
        return f"Asset {self.asset_id} loaned to {self.learner_username}"