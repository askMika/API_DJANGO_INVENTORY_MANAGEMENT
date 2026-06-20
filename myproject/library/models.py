from django.db import models
from datetime import date

class BorrowedBooks(models.Model):
    id = models.AutoField(primary_key=True)
    learner_id = models.CharField(max_length=50)
    asset_id = models.IntegerField()  
    borrowed_date = models.DateField(default=date.today)
    
    # DurationField handles PostgreSQL intervals natively behind the scenes
    loan_period = models.DurationField(help_text="Expected format: 'DD HH:MM:SS'")
    due_date = models.DateField()
    librarian_id = models.CharField(max_length=50)
    
    status = models.CharField(
        max_length=20, 
        default='Active', 
        choices=[('Active', 'Active'), ('Returned', 'Returned'), ('Overdue', 'Overdue')]
    )

    class Meta:
        db_table = 'borrowed_books'  # Forces clean lowercase database table binding
        ordering = ['-due_date']     # Puts closest upcoming deadlines at the top of query sets

    def __str__(self):
        return f"Asset {self.asset_id} borrowed by Learner {self.learner_id}"