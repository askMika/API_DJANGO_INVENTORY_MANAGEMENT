from django.urls import path
#from .views import BorrowBookView, ReturnBookView
#from .views import BookStockItemListView
from .views import getAll, addBorrowedBook,getAllBooks

urlpatterns = [
    path('BorrowedBooks/all/', getAll, name='borrow-get-all'),
    path('BorrowedBooks/add/', addBorrowedBook, name='borrow-add-new'),
    path('books/getAll',getAllBooks,name="get-all-books"),
]

