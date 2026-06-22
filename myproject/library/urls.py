from django.urls import path
#from .views import BorrowBookView, ReturnBookView
#from .views import BookStockItemListView
from .views import getAll, addBorrowedBook

urlpatterns = [
path('BorrowedBooks/all/', getAll, name='borrow-get-all'),
    path('BorrowedBooks/add/', addBorrowedBook, name='borrow-add-new'),
    
]

